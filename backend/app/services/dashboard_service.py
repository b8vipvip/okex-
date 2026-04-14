from decimal import Decimal

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.enums import TaskStatus
from app.models.recharge_task import RechargeTask


class DashboardService:
    @staticmethod
    def stats(db: Session):
        total = db.scalar(select(func.count()).select_from(RechargeTask)) or 0

        status_counts = {s.value: 0 for s in TaskStatus}
        rows = db.execute(select(RechargeTask.status, func.count()).group_by(RechargeTask.status)).all()
        for status, count in rows:
            status_counts[status.value] = count

        sums = db.execute(
            select(
                func.coalesce(func.sum(RechargeTask.sale_price), 0),
                func.coalesce(func.sum(RechargeTask.recharge_cost), 0),
                func.coalesce(func.sum(RechargeTask.profit), 0),
            )
        ).one()
        sale_total, cost_total, profit_total = sums

        return {
            "total_tasks": total,
            **status_counts,
            "sale_total": Decimal(sale_total),
            "cost_total": Decimal(cost_total),
            "profit_total": Decimal(profit_total),
        }
