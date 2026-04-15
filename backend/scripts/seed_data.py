from decimal import Decimal

from app.db.session import SessionLocal
from app.models.enums import PlanType
from app.services.task_service import TaskService


def run():
    db = SessionLocal()
    try:
        sample = """10001----测试A
10002----测试B
10003----测试C"""
        TaskService.import_tasks(db, "初始化批次", PlanType.month, Decimal("25.00"), sample)
        print("seed done")
    finally:
        db.close()


if __name__ == "__main__":
    run()
