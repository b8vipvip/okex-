"""init

Revision ID: 20260414_0001
Revises: 
Create Date: 2026-04-14
"""

from alembic import op
import sqlalchemy as sa

revision = "20260414_0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "task_batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("batch_no", sa.String(length=64), nullable=False),
        sa.Column("batch_name", sa.String(length=128), nullable=False),
        sa.Column("total_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("success_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("failed_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("pending_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("uploaded_by", sa.String(length=64), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_task_batches_batch_no", "task_batches", ["batch_no"], unique=True)

    op.create_table(
        "workers",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("worker_id", sa.String(length=64), nullable=False),
        sa.Column("worker_name", sa.String(length=128), nullable=True),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("last_heartbeat_at", sa.DateTime(), nullable=True),
        sa.Column("current_task_id", sa.Integer(), nullable=True),
        sa.Column("concurrency_limit", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_workers_worker_id", "workers", ["worker_id"], unique=True)

    op.create_table(
        "recharge_tasks",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_no", sa.String(length=64), nullable=False),
        sa.Column("source_batch_id", sa.Integer(), sa.ForeignKey("task_batches.id"), nullable=False),
        sa.Column("account_identifier", sa.String(length=128), nullable=False),
        sa.Column("account_remark", sa.String(length=255), nullable=True),
        sa.Column("plan_type", sa.Enum("month", "season", "year", name="plantype"), nullable=False),
        sa.Column("sale_price", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"),
        sa.Column("recharge_cost", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"),
        sa.Column("profit", sa.DECIMAL(10, 2), nullable=False, server_default="0.00"),
        sa.Column("kugou_id", sa.String(length=128), nullable=True),
        sa.Column("validity_value", sa.Integer(), nullable=True),
        sa.Column("validity_unit", sa.String(length=16), nullable=True),
        sa.Column("app_month_price", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("app_season_price", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("app_year_price", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("web_month_price", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("web_season_price", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("web_year_price", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("pc_month_price", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("pc_season_price", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("pc_year_price", sa.DECIMAL(10, 2), nullable=True),
        sa.Column("status", sa.Enum("pending", "queued", "claimed", "processing", "success", "failed", "cancelled", name="taskstatus"), nullable=False),
        sa.Column("fail_code", sa.String(length=64), nullable=True),
        sa.Column("fail_reason", sa.Text(), nullable=True),
        sa.Column("uploaded_at", sa.DateTime(), nullable=False),
        sa.Column("queued_at", sa.DateTime(), nullable=True),
        sa.Column("claimed_at", sa.DateTime(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("failed_at", sa.DateTime(), nullable=True),
        sa.Column("worker_id", sa.String(length=64), nullable=True),
        sa.Column("retry_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    for name, cols, unique in [
        ("ix_recharge_tasks_task_no", ["task_no"], True),
        ("ix_recharge_tasks_source_batch_id", ["source_batch_id"], False),
        ("ix_recharge_tasks_account_identifier", ["account_identifier"], False),
        ("ix_recharge_tasks_plan_type", ["plan_type"], False),
        ("ix_recharge_tasks_status", ["status"], False),
        ("ix_recharge_tasks_worker_id", ["worker_id"], False),
        ("ix_recharge_tasks_kugou_id", ["kugou_id"], False),
    ]:
        op.create_index(name, "recharge_tasks", cols, unique=unique)
    op.create_index("idx_task_query_combo", "recharge_tasks", ["status", "plan_type", "source_batch_id", "worker_id"])

    op.create_table(
        "task_logs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("task_id", sa.Integer(), sa.ForeignKey("recharge_tasks.id"), nullable=False),
        sa.Column("worker_id", sa.String(length=64), nullable=True),
        sa.Column("action", sa.String(length=64), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_task_logs_task_id", "task_logs", ["task_id"])


def downgrade() -> None:
    op.drop_table("task_logs")
    op.drop_table("recharge_tasks")
    op.drop_table("workers")
    op.drop_table("task_batches")
