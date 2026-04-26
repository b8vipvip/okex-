from datetime import datetime

from app.schemas.common import ORMBase


class BatchOut(ORMBase):
    id: int
    batch_no: str
    batch_name: str
    total_count: int
    success_count: int
    failed_count: int
    pending_count: int
    uploaded_by: str | None
    created_at: datetime
