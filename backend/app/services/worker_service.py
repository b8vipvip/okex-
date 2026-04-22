from datetime import datetime

from sqlalchemy import func, select, update
from sqlalchemy.orm import Session

from app.models.enums import TaskStatus
from app.models.recharge_task import RechargeTask
from app.models.task_log import TaskLog
from app.models.worker import Worker


class WorkerService:
    CLAIM_RETRY_TIMES = 5

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
        for _ in range(WorkerService.CLAIM_RETRY_TIMES):
            task_id = db.scalar(
                select(RechargeTask.id)
                .where(RechargeTask.status == TaskStatus.queued)
                .order_by(RechargeTask.id.asc())
                .limit(1)
            )
            if not task_id:
                db.rollback()
                return None

            claim_result = db.execute(
                update(RechargeTask)
                .where(RechargeTask.id == task_id, RechargeTask.status == TaskStatus.queued)
                .values(status=TaskStatus.claimed, worker_id=worker_id, claimed_at=func.now())
            )

            if claim_result.rowcount == 1:
                task = db.get(RechargeTask, task_id)
                db.add(TaskLog(task_id=task_id, worker_id=worker_id, action="status_change", content="queued -> claimed"))

                worker = db.scalar(select(Worker).where(Worker.worker_id == worker_id))
                if worker:
                    worker.current_task_id = task_id

                db.commit()
                db.refresh(task)
                return task

            db.rollback()

        return None
