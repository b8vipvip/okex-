from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlalchemy.orm import Session

from app.api.deps import AdminUser, WorkerAuth
from app.core.response import ok
from app.db.session import get_db
from app.models.enums import TaskStatus
from app.models.recharge_task import RechargeTask
from app.schemas.task import TaskFailIn, TaskFilter, TaskImportIn, TaskOut, TaskProgressIn, TaskStartIn, TaskSuccessIn
from app.services.task_service import TaskService

router = APIRouter(prefix="/api/tasks", tags=["tasks"])


@router.post("/import")
async def import_tasks(
    batch_name: str = Form(...),
    plan_type: str = Form(...),
    sale_price: str = Form(...),
    text_content: str = Form(""),
    file: UploadFile | None = File(default=None),
    _: str = AdminUser,
    db: Session = Depends(get_db),
):
    file_content = ""
    if file is not None:
        file_content = (await file.read()).decode("utf-8", errors="ignore")
    payload = TaskImportIn(batch_name=batch_name, plan_type=plan_type, sale_price=sale_price, text_content=text_content or file_content)
    batch, stats = TaskService.import_tasks(db, payload.batch_name, payload.plan_type, payload.sale_price, payload.text_content)
    return ok({"batch_id": batch.id, "batch_no": batch.batch_no, **stats})


@router.get("")
def list_tasks(
    page: int = 1,
    page_size: int = 20,
    status: TaskStatus | None = None,
    plan_type: str | None = None,
    batch_id: int | None = None,
    worker_id: str | None = None,
    keyword: str | None = None,
    start_time: str | None = None,
    end_time: str | None = None,
    _: str = AdminUser,
    db: Session = Depends(get_db),
):
    query = TaskFilter(
        page=page,
        page_size=page_size,
        status=status,
        plan_type=plan_type,
        batch_id=batch_id,
        worker_id=worker_id,
        keyword=keyword,
        start_time=start_time,
        end_time=end_time,
    )
    total, items = TaskService.list_tasks(db, query)
    return ok({"total": total, "page": page, "page_size": page_size, "items": [TaskOut.model_validate(x).model_dump() for x in items]})


@router.get("/{task_id}")
def task_detail(task_id: int, _: str = AdminUser, db: Session = Depends(get_db)):
    task = TaskService.get_task(db, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    data = TaskOut.model_validate(task).model_dump()
    data["logs"] = [{"id": x.id, "action": x.action, "content": x.content, "worker_id": x.worker_id, "created_at": x.created_at} for x in sorted(task.logs, key=lambda l: l.id)]
    data.update({"fail_code": task.fail_code, "validity_value": task.validity_value, "validity_unit": task.validity_unit, "claimed_at": task.claimed_at, "queued_at": task.queued_at, "failed_at": task.failed_at})
    return ok(data)


@router.post("/{task_id}/start")
def start_task(task_id: int, payload: TaskStartIn, _: str = WorkerAuth, db: Session = Depends(get_db)):
    task = db.get(RechargeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    if task.status != TaskStatus.claimed or task.worker_id != payload.worker_id:
        raise HTTPException(status_code=400, detail="task not in claimed status for this worker")
    TaskService.start_task(db, task, payload.worker_id)
    return ok({"task_id": task_id})


@router.post("/{task_id}/success")
def success_task(task_id: int, payload: TaskSuccessIn, _: str = WorkerAuth, db: Session = Depends(get_db)):
    task = db.get(RechargeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    if task.status != TaskStatus.processing or task.worker_id != payload.worker_id:
        raise HTTPException(status_code=400, detail="task not in processing status for this worker")
    TaskService.success_task(db, task, payload)
    return ok({"task_id": task_id, "status": "success"})


@router.post("/{task_id}/fail")
def fail_task(task_id: int, payload: TaskFailIn, _: str = WorkerAuth, db: Session = Depends(get_db)):
    task = db.get(RechargeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    if task.status != TaskStatus.processing or task.worker_id != payload.worker_id:
        raise HTTPException(status_code=400, detail="task not in processing status for this worker")
    TaskService.fail_task(db, task, payload)
    return ok({"task_id": task_id, "status": "failed"})


@router.post("/{task_id}/progress")
def report_task_progress(task_id: int, payload: TaskProgressIn, _: str = WorkerAuth, db: Session = Depends(get_db)):
    task = db.get(RechargeTask, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="task not found")
    if task.worker_id != payload.worker_id:
        raise HTTPException(status_code=400, detail="task not assigned to this worker")
    if task.status not in (TaskStatus.claimed, TaskStatus.processing):
        raise HTTPException(status_code=400, detail="task not in claimed or processing status")
    TaskService.update_progress(db, task, payload.worker_id, payload.progress_status)
    return ok({"task_id": task_id, "progress_status": payload.progress_status})
