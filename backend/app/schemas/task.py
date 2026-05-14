from datetime import datetime
from decimal import Decimal
from typing import Annotated

from pydantic import BaseModel, BeforeValidator, Field

from app.models.enums import PlanType, TaskStatus, TaskType
from app.schemas.common import ORMBase


def blank_to_none(value):
    if isinstance(value, str) and value.strip() == "":
        return None
    return value


OptionalDecimal = Annotated[Decimal | None, BeforeValidator(blank_to_none), Field(ge=0)]
OptionalProfit = Annotated[Decimal | None, BeforeValidator(blank_to_none)]
OptionalInt = Annotated[int | None, BeforeValidator(blank_to_none)]
OptionalStr = Annotated[str | None, BeforeValidator(blank_to_none)]
OptionalDateTime = Annotated[datetime | None, BeforeValidator(blank_to_none)]


class TaskImportIn(BaseModel):
    batch_name: str = Field(min_length=1, max_length=128)
    plan_type: PlanType
    task_type: TaskType = TaskType.recharge
    sale_price: Decimal = Field(ge=0)
    text_content: str = ""


class TaskFilter(BaseModel):
    page: int = 1
    page_size: int = 20
    status: TaskStatus | None = None
    plan_type: PlanType | None = None
    task_type: TaskType | None = None
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
    task_type: TaskType
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


class TaskPriceOut(ORMBase):
    task_no: str
    task_type: TaskType
    status: TaskStatus
    account_identifier: str
    account_remark: str | None
    app_month_price: Decimal | None
    app_season_price: Decimal | None
    app_year_price: Decimal | None
    web_month_price: Decimal | None
    web_season_price: Decimal | None
    web_year_price: Decimal | None
    pc_month_price: Decimal | None
    pc_season_price: Decimal | None
    pc_year_price: Decimal | None
    super_month_price: Decimal | None
    app_promo_super_month_price: Decimal | None
    web_promo_super_month_price: Decimal | None
    started_at: datetime | None


class TaskAdminUpdateIn(BaseModel):
    task_no: OptionalStr = Field(default=None, max_length=64)
    source_batch_id: OptionalInt = None
    account_identifier: OptionalStr = Field(default=None, max_length=128)
    account_remark: OptionalStr = Field(default=None, max_length=255)
    plan_type: PlanType | None = None
    task_type: TaskType | None = None
    sale_price: OptionalDecimal = None
    recharge_cost: OptionalDecimal = None
    profit: OptionalProfit = None
    kugou_id: OptionalStr = Field(default=None, max_length=128)
    validity_value: OptionalInt = None
    validity_unit: OptionalStr = Field(default=None, max_length=16)
    app_month_price: OptionalDecimal = None
    app_season_price: OptionalDecimal = None
    app_year_price: OptionalDecimal = None
    web_month_price: OptionalDecimal = None
    web_season_price: OptionalDecimal = None
    web_year_price: OptionalDecimal = None
    pc_month_price: OptionalDecimal = None
    pc_season_price: OptionalDecimal = None
    pc_year_price: OptionalDecimal = None
    super_month_price: OptionalDecimal = None
    app_promo_super_month_price: OptionalDecimal = None
    web_promo_super_month_price: OptionalDecimal = None
    status: TaskStatus | None = None
    progress_status: OptionalStr = Field(default=None, max_length=100)
    progress_updated_at: OptionalDateTime = None
    fail_code: OptionalStr = Field(default=None, max_length=64)
    fail_reason: OptionalStr = None
    uploaded_at: OptionalDateTime = None
    queued_at: OptionalDateTime = None
    claimed_at: OptionalDateTime = None
    started_at: OptionalDateTime = None
    finished_at: OptionalDateTime = None
    failed_at: OptionalDateTime = None
    created_at: OptionalDateTime = None
    worker_id: OptionalStr = Field(default=None, max_length=64)
    retry_count: OptionalInt = None


class TaskBatchUpdateIn(BaseModel):
    task_ids: list[int] = Field(min_length=1)
    updates: TaskAdminUpdateIn


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
    worker_id: str = Field(min_length=1)
    kugou_id: OptionalStr = None
    validity_value: OptionalInt = None
    validity_unit: OptionalStr = None
    sale_price: OptionalDecimal = None
    recharge_cost: OptionalDecimal = None
    app_month_price: OptionalDecimal = None
    app_season_price: OptionalDecimal = None
    app_year_price: OptionalDecimal = None
    web_month_price: OptionalDecimal = None
    web_season_price: OptionalDecimal = None
    web_year_price: OptionalDecimal = None
    pc_month_price: OptionalDecimal = None
    pc_season_price: OptionalDecimal = None
    pc_year_price: OptionalDecimal = None
    super_month_price: OptionalDecimal = None
    app_promo_super_month_price: OptionalDecimal = None
    web_promo_super_month_price: OptionalDecimal = None
    progress_status: OptionalStr = Field(default=None, max_length=100)


class TaskPriceProgressIn(BaseModel):
    worker_id: str = Field(min_length=1)
    kugou_id: OptionalStr = None
    app_month_price: OptionalDecimal = None
    app_season_price: OptionalDecimal = None
    app_year_price: OptionalDecimal = None
    web_month_price: OptionalDecimal = None
    web_season_price: OptionalDecimal = None
    web_year_price: OptionalDecimal = None
    pc_month_price: OptionalDecimal = None
    pc_season_price: OptionalDecimal = None
    pc_year_price: OptionalDecimal = None
    super_month_price: OptionalDecimal = None
    app_promo_super_month_price: OptionalDecimal = None
    web_promo_super_month_price: OptionalDecimal = None
    progress_status: OptionalStr = Field(default=None, max_length=100)


class TaskFailIn(BaseModel):
    worker_id: str
    fail_code: str
    fail_reason: str


class TaskProgressIn(BaseModel):
    worker_id: str
    progress_status: str = Field(min_length=1, max_length=100)
