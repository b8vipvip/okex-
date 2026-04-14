from pydantic import BaseModel


class WorkerHeartbeatIn(BaseModel):
    worker_id: str
    worker_name: str | None = None
    concurrency_limit: int = 1


class WorkerClaimIn(BaseModel):
    worker_id: str
