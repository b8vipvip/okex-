from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.models.enums import TaskStatus, TaskType
from app.models.recharge_task import RechargeTask
from app.models.task_log import TaskLog
from app.models.worker import Worker
from app.utils.time import now_cn


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
        current_time = now_cn()
        worker.last_heartbeat_at = current_time
        worker.updated_at = current_time
        db.commit()
        return worker

    @staticmethod
    def claim_task(db: Session, worker_id: str, task_type: TaskType | None = None):
        for _ in range(WorkerService.CLAIM_RETRY_TIMES):
            task_id = db.scalar(
                select(RechargeTask.id)
                .where(
                    RechargeTask.status == TaskStatus.queued,
                    *([RechargeTask.task_type == task_type] if task_type else []),
                )
                .order_by(RechargeTask.id.asc())
                .limit(1)
            )
            if not task_id:
                db.rollback()
                return None

            current_time = now_cn()
            claim_result = db.execute(
                update(RechargeTask)
                .where(RechargeTask.id == task_id, RechargeTask.status == TaskStatus.queued)
                .values(status=TaskStatus.claimed, worker_id=worker_id, claimed_at=current_time, updated_at=current_time)
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
