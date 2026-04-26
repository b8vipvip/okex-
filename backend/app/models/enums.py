from enum import Enum


class PlanType(str, Enum):
    month = "month"
    season = "season"
    year = "year"


class TaskStatus(str, Enum):
    pending = "pending"
    queued = "queued"
    claimed = "claimed"
    processing = "processing"
    success = "success"
    failed = "failed"
    cancelled = "cancelled"
