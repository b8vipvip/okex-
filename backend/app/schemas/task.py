from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.enums import PlanType, TaskStatus
from app.schemas.common import ORMBase


class TaskImportIn(BaseModel):
    batch_name: str = Field(min_length=1, max_length=128)
    plan_type: PlanType
    sale_price: Decimal = Field(ge=0)
    text_content: str = ""


class TaskFilter(BaseModel):
    page: int = 1
    page_size: int = 20
    status: TaskStatus | None = None
    plan_type: PlanType | None = None
    batch_id: int | None = None
    worker_id: str | None = None
    keyword: str | None = None
    start_time: datetime | None = None
    end_time: datetime | None = None


class TaskOut(ORMBase):
    id: int
    task_no: str
    source_batch_id: int
    account_identifier: str
    account_remark: str | None
    plan_type: PlanType
    sale_price: Decimal
    recharge_cost: Decimal
    profit: Decimal
    kugou_id: str | None
    status: TaskStatus
    progress_status: str | None
    progress_updated_at: datetime | None
    worker_id: str | None
    uploaded_at: datetime
    started_at: datetime | None
    finished_at: datetime | None
    fail_reason: str | None


class TaskLogOut(ORMBase):
    id: int
    action: str
    content: str
    worker_id: str | None
    created_at: datetime


class TaskDetailOut(TaskOut):
    fail_code: str | None
    validity_value: int | None
    validity_unit: str | None
    claimed_at: datetime | None
    queued_at: datetime | None
    failed_at: datetime | None
    logs: list[TaskLogOut]


class TaskStartIn(BaseModel):
    worker_id: str


class TaskSuccessIn(BaseModel):
    worker_id: str
    kugou_id: str
    recharge_cost: Decimal = Field(ge=0)
    validity_value: int
    validity_unit: str
    app_month_price: Decimal | None = None
    app_season_price: Decimal | None = None
    app_year_price: Decimal | None = None
    web_month_price: Decimal | None = None
    web_season_price: Decimal | None = None
    web_year_price: Decimal | None = None
    pc_month_price: Decimal | None = None
    pc_season_price: Decimal | None = None
    pc_year_price: Decimal | None = None


class TaskFailIn(BaseModel):
    worker_id: str
    fail_code: str
    fail_reason: str


class TaskProgressIn(BaseModel):
    worker_id: str
    progress_status: str = Field(min_length=1, max_length=100)
