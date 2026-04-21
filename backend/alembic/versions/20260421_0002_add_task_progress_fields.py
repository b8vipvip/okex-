"""add task progress fields

Revision ID: 20260421_0002
Revises: 20260414_0001
Create Date: 2026-04-21
"""

from alembic import op
import sqlalchemy as sa


revision = "20260421_0002"
down_revision = "20260414_0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("recharge_tasks", sa.Column("progress_status", sa.String(length=100), nullable=True))
    op.add_column("recharge_tasks", sa.Column("progress_updated_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    op.drop_column("recharge_tasks", "progress_updated_at")
    op.drop_column("recharge_tasks", "progress_status")
