from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import AdminUser
from app.core.response import ok
from app.db.session import get_db
from app.models.task_batch import TaskBatch
from app.schemas.batch import BatchOut

router = APIRouter(prefix="/api/batches", tags=["batches"])


@router.get("")
def list_batches(_: str = AdminUser, db: Session = Depends(get_db)):
    items = db.scalars(select(TaskBatch).order_by(TaskBatch.id.desc())).all()
    return ok([BatchOut.model_validate(x).model_dump() for x in items])


@router.get("/{batch_id}")
def batch_detail(batch_id: int, _: str = AdminUser, db: Session = Depends(get_db)):
    batch = db.get(TaskBatch, batch_id)
    if not batch:
        raise HTTPException(status_code=404, detail="batch not found")
    return ok(BatchOut.model_validate(batch).model_dump())
