from enum import Enum


class PlanType(str, Enum):
    month = "month"
    season = "season"
    year = "year"


class TaskType(str, Enum):
    recharge = "充值"
    query_price = "查询价格"


class TaskStatus(str, Enum):
    pending = "pending"
    queued = "queued"
    claimed = "claimed"
    processing = "processing"
    success = "success"
    failed = "failed"
    cancelled = "cancelled"
