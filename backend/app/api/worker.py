from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import WorkerAuth
from app.core.response import ok
from app.db.session import get_db
from app.schemas.task import TaskOut
from app.schemas.worker import WorkerClaimIn, WorkerHeartbeatIn
from app.services.worker_service import WorkerService

router = APIRouter(prefix="/api/worker", tags=["worker"])


@router.post("/heartbeat")
def heartbeat(payload: WorkerHeartbeatIn, _: str = WorkerAuth, db: Session = Depends(get_db)):
    worker = WorkerService.heartbeat(db, payload.worker_id, payload.worker_name, payload.concurrency_limit)
    return ok({"worker_id": worker.worker_id, "last_heartbeat_at": worker.last_heartbeat_at})


@router.post("/claim")
def claim(payload: WorkerClaimIn, _: str = WorkerAuth, db: Session = Depends(get_db)):
    task = WorkerService.claim_task(db, payload.worker_id)
    if not task:
        return ok(None, message="no queued task")
    return ok(TaskOut.model_validate(task).model_dump())
