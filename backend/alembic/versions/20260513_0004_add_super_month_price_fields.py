"""add super month price fields

Revision ID: 20260513_0004
Revises: 20260426_0003
Create Date: 2026-05-13
"""

from alembic import op
import sqlalchemy as sa

revision = "20260513_0004"
down_revision = "20260426_0003"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("recharge_tasks", sa.Column("super_month_price", sa.DECIMAL(10, 2), nullable=True, comment="超级一个月价格"))
    op.add_column("recharge_tasks", sa.Column("app_promo_super_month_price", sa.DECIMAL(10, 2), nullable=True, comment="APP特惠超级一个月价格"))
    op.add_column("recharge_tasks", sa.Column("web_promo_super_month_price", sa.DECIMAL(10, 2), nullable=True, comment="WEB特惠超级一个月价格"))


def downgrade() -> None:
    op.drop_column("recharge_tasks", "web_promo_super_month_price")
    op.drop_column("recharge_tasks", "app_promo_super_month_price")
    op.drop_column("recharge_tasks", "super_month_price")
