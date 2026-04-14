from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import AdminUser
from app.core.response import ok
from app.db.session import get_db
from app.services.dashboard_service import DashboardService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats")
def stats(_: str = AdminUser, db: Session = Depends(get_db)):
    return ok(DashboardService.stats(db))
