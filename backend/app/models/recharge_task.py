from datetime import datetime
from decimal import Decimal

from sqlalchemy import DECIMAL, DateTime, Enum, ForeignKey, Index, Integer, String, Text, event
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.enums import PlanType, TaskStatus


class RechargeTask(Base):
    __tablename__ = "recharge_tasks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    task_no: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    source_batch_id: Mapped[int] = mapped_column(ForeignKey("task_batches.id"), index=True)
    account_identifier: Mapped[str] = mapped_column(String(128), index=True)
    account_remark: Mapped[str | None] = mapped_column(String(255), nullable=True)

    plan_type: Mapped[PlanType] = mapped_column(Enum(PlanType), index=True)
    sale_price: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=Decimal("0.00"))
    recharge_cost: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=Decimal("0.00"))
    profit: Mapped[Decimal] = mapped_column(DECIMAL(10, 2), default=Decimal("0.00"))

    kugou_id: Mapped[str | None] = mapped_column(String(128), nullable=True, index=True)
    validity_value: Mapped[int | None] = mapped_column(Integer, nullable=True)
    validity_unit: Mapped[str | None] = mapped_column(String(16), nullable=True)

    app_month_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)
    app_season_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)
    app_year_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)

    web_month_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)
    web_season_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)
    web_year_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)

    pc_month_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)
    pc_season_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)
    pc_year_price: Mapped[Decimal | None] = mapped_column(DECIMAL(10, 2), nullable=True)

    status: Mapped[TaskStatus] = mapped_column(Enum(TaskStatus), index=True, default=TaskStatus.pending)
    progress_status: Mapped[str | None] = mapped_column(String(100), nullable=True)
    progress_updated_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    fail_code: Mapped[str | None] = mapped_column(String(64), nullable=True)
    fail_reason: Mapped[str | None] = mapped_column(Text, nullable=True)

    uploaded_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    queued_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    claimed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    finished_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    failed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    worker_id: Mapped[str | None] = mapped_column(String(64), index=True, nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    batch = relationship("TaskBatch", back_populates="tasks")
    logs = relationship("TaskLog", back_populates="task", cascade="all, delete-orphan")

    __table_args__ = (
        Index("idx_task_query_combo", "status", "plan_type", "source_batch_id", "worker_id"),
    )


@event.listens_for(RechargeTask.progress_status, "set", retval=False)
def update_progress_updated_at_on_status_change(target: RechargeTask, value: str | None, oldvalue: str | None, initiator):
    if value != oldvalue:
        target.progress_updated_at = datetime.utcnow()
