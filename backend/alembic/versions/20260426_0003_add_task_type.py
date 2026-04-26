"""add task type

Revision ID: 20260426_0003
Revises: 20260421_0002
Create Date: 2026-04-26
"""

from alembic import op
import sqlalchemy as sa


revision = "20260426_0003"
down_revision = "20260421_0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "recharge_tasks",
        sa.Column("task_type", sa.Enum("充值", "查询价格", name="tasktype"), nullable=False, server_default="充值"),
    )
    op.create_index("ix_recharge_tasks_task_type", "recharge_tasks", ["task_type"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_recharge_tasks_task_type", table_name="recharge_tasks")
    op.drop_column("recharge_tasks", "task_type")
