from datetime import datetime

from sqlalchemy import select, text
from sqlalchemy.exc import ProgrammingError
from sqlalchemy.orm import Session

from app.models.enums import TaskStatus
from app.models.recharge_task import RechargeTask
from app.models.task_log import TaskLog
from app.models.worker import Worker


class WorkerService:
    @staticmethod
    def heartbeat(db: Session, worker_id: str, worker_name: str | None, concurrency_limit: int):
        worker = db.scalar(select(Worker).where(Worker.worker_id == worker_id))
        if not worker:
            worker = Worker(worker_id=worker_id)
            db.add(worker)
        worker.worker_name = worker_name or worker.worker_name
        worker.status = "online"
        worker.concurrency_limit = concurrency_limit
        worker.last_heartbeat_at = datetime.utcnow()
        db.commit()
        return worker

    @staticmethod
    def _finalize_claim(db: Session, task: RechargeTask, worker_id: str):
        db.add(TaskLog(task_id=task.id, worker_id=worker_id, action="status_change", content="queued -> claimed"))
        worker = db.scalar(select(Worker).where(Worker.worker_id == worker_id))
        if worker:
            worker.current_task_id = task.id
        db.commit()
        db.refresh(task)
        return task

    @staticmethod
    def _claim_with_skip_locked(db: Session, worker_id: str):
        stmt = (
            select(RechargeTask)
            .where(RechargeTask.status == TaskStatus.queued)
            .order_by(RechargeTask.id.asc())
            .with_for_update(skip_locked=True)
            .limit(1)
        )
        task = db.scalar(stmt)
        if not task:
            db.commit()
            return None
        task.status = TaskStatus.claimed
        task.worker_id = worker_id
        task.claimed_at = datetime.utcnow()
        return WorkerService._finalize_claim(db, task, worker_id)

    @staticmethod
    def _claim_with_compat_update(db: Session, worker_id: str):
        claimed_at = datetime.utcnow()
        sql = text(
            """
            UPDATE recharge_tasks
            SET status = :claimed_status,
                worker_id = :worker_id,
                claimed_at = :claimed_at
            WHERE id = (
                SELECT id FROM (
                    SELECT id
                    FROM recharge_tasks
                    WHERE status = :queued_status
                    ORDER BY id ASC
                    LIMIT 1
                ) AS q
            )
            AND status = :queued_status
            """
        )
        result = db.execute(
            sql,
            {
                "claimed_status": TaskStatus.claimed.value,
                "queued_status": TaskStatus.queued.value,
                "worker_id": worker_id,
                "claimed_at": claimed_at,
            },
        )
        if result.rowcount == 0:
            db.commit()
            return None

        task = db.scalar(
            select(RechargeTask)
            .where(RechargeTask.worker_id == worker_id, RechargeTask.status == TaskStatus.claimed)
            .order_by(RechargeTask.claimed_at.desc(), RechargeTask.id.desc())
            .limit(1)
        )
        if not task:
            db.commit()
            return None
        return WorkerService._finalize_claim(db, task, worker_id)

    @staticmethod
    def claim_task(db: Session, worker_id: str):
        try:
            return WorkerService._claim_with_skip_locked(db, worker_id)
        except ProgrammingError as exc:
            db.rollback()
            if "SKIP LOCKED" not in str(exc).upper():
                raise
            return WorkerService._claim_with_compat_update(db, worker_id)
