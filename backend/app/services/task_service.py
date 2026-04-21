from datetime import datetime
from decimal import Decimal
from uuid import uuid4

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session, joinedload

from app.models.enums import TaskStatus
from app.models.recharge_task import RechargeTask
from app.models.task_batch import TaskBatch
from app.models.task_log import TaskLog


class TaskService:
    @staticmethod
    def _log(db: Session, task_id: int, action: str, content: str, worker_id: str | None = None):
        db.add(TaskLog(task_id=task_id, action=action, content=content, worker_id=worker_id))

    @staticmethod
    def import_tasks(db: Session, batch_name: str, plan_type: str, sale_price: Decimal, raw_text: str, uploaded_by: str = "admin"):
        lines = raw_text.splitlines()
        stats = {"total_lines": len(lines), "success_count": 0, "duplicate_count": 0, "format_error_count": 0, "skipped_count": 0}

        batch = TaskBatch(
            batch_no=f"B{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{str(uuid4())[:4]}",
            batch_name=batch_name,
            uploaded_by=uploaded_by,
        )
        db.add(batch)
        db.flush()

        seen: set[str] = set()
        for line in lines:
            stripped = line.strip()
            if not stripped:
                stats["skipped_count"] += 1
                continue
            parts = stripped.split("----")
            if len(parts) != 2 or not parts[0].strip():
                stats["format_error_count"] += 1
                continue
            account_identifier = parts[0].strip()
            remark = parts[1].strip()
            key = f"{account_identifier}::{remark}"
            if key in seen:
                stats["duplicate_count"] += 1
                continue
            seen.add(key)
            task = RechargeTask(
                task_no=f"T{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{str(uuid4())[:8]}",
                source_batch_id=batch.id,
                account_identifier=account_identifier,
                account_remark=remark,
                plan_type=plan_type,
                sale_price=sale_price,
                status=TaskStatus.pending,
                uploaded_at=datetime.utcnow(),
            )
            db.add(task)
            db.flush()
            TaskService._log(db, task.id, "status_change", "pending -> queued")
            task.status = TaskStatus.queued
            task.queued_at = datetime.utcnow()
            stats["success_count"] += 1

        batch.total_count = stats["success_count"]
        batch.pending_count = stats["success_count"]
        db.commit()
        return batch, stats

    @staticmethod
    def list_tasks(db: Session, query):
        stmt = select(RechargeTask)
        if query.status:
            stmt = stmt.where(RechargeTask.status == query.status)
        if query.plan_type:
            stmt = stmt.where(RechargeTask.plan_type == query.plan_type)
        if query.batch_id:
            stmt = stmt.where(RechargeTask.source_batch_id == query.batch_id)
        if query.worker_id:
            stmt = stmt.where(RechargeTask.worker_id == query.worker_id)
        if query.keyword:
            kw = f"%{query.keyword}%"
            stmt = stmt.where(or_(RechargeTask.account_identifier.like(kw), RechargeTask.kugou_id.like(kw), RechargeTask.task_no.like(kw)))
        if query.start_time:
            stmt = stmt.where(RechargeTask.created_at >= query.start_time)
        if query.end_time:
            stmt = stmt.where(RechargeTask.created_at <= query.end_time)

        total = db.scalar(select(func.count()).select_from(stmt.subquery()))
        items = db.scalars(stmt.order_by(RechargeTask.id.desc()).offset((query.page - 1) * query.page_size).limit(query.page_size)).all()
        return total or 0, items

    @staticmethod
    def get_task(db: Session, task_id: int):
        stmt = select(RechargeTask).options(joinedload(RechargeTask.logs)).where(RechargeTask.id == task_id)
        return db.scalar(stmt)

    @staticmethod
    def start_task(db: Session, task: RechargeTask, worker_id: str):
        task.status = TaskStatus.processing
        task.started_at = datetime.utcnow()
        TaskService._log(db, task.id, "status_change", "claimed -> processing", worker_id)
        db.commit()

    @staticmethod
    def success_task(db: Session, task: RechargeTask, payload):
        task.status = TaskStatus.success
        task.progress_status = "充值完成"
        task.kugou_id = payload.kugou_id
        task.recharge_cost = payload.recharge_cost
        task.validity_value = payload.validity_value
        task.validity_unit = payload.validity_unit
        for field in [
            "app_month_price",
            "app_season_price",
            "app_year_price",
            "web_month_price",
            "web_season_price",
            "web_year_price",
            "pc_month_price",
            "pc_season_price",
            "pc_year_price",
        ]:
            setattr(task, field, getattr(payload, field))
        task.profit = (task.sale_price or Decimal("0.00")) - (task.recharge_cost or Decimal("0.00"))
        task.finished_at = datetime.utcnow()
        TaskService._log(db, task.id, "status_change", "processing -> success", payload.worker_id)
        TaskService._log(db, task.id, "progress_update", task.progress_status, payload.worker_id)

        batch = db.get(TaskBatch, task.source_batch_id)
        if batch:
            batch.success_count += 1
            batch.pending_count = max(batch.pending_count - 1, 0)
        db.commit()

    @staticmethod
    def fail_task(db: Session, task: RechargeTask, payload):
        task.status = TaskStatus.failed
        task.progress_status = payload.fail_reason or "充值失败"
        task.fail_code = payload.fail_code
        task.fail_reason = payload.fail_reason
        task.failed_at = datetime.utcnow()
        TaskService._log(db, task.id, "status_change", f"processing -> failed ({payload.fail_code})", payload.worker_id)
        TaskService._log(db, task.id, "progress_update", task.progress_status, payload.worker_id)
        batch = db.get(TaskBatch, task.source_batch_id)
        if batch:
            batch.failed_count += 1
            batch.pending_count = max(batch.pending_count - 1, 0)
        db.commit()

    @staticmethod
    def update_progress(db: Session, task: RechargeTask, worker_id: str, progress_status: str):
        task.progress_status = progress_status
        TaskService._log(db, task.id, "progress_update", progress_status, worker_id)
        db.commit()
