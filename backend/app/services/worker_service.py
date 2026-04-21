from datetime import datetime

from sqlalchemy import select
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
    def claim_task(db: Session, worker_id: str):
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
        db.add(TaskLog(task_id=task.id, worker_id=worker_id, action="status_change", content="queued -> claimed"))

        worker = db.scalar(select(Worker).where(Worker.worker_id == worker_id))
        if worker:
            worker.current_task_id = task.id
        db.commit()
        db.refresh(task)
        return task
