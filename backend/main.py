from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.batches import router as batches_router
from app.api.dashboard import router as dashboard_router
from app.api.tasks import router as tasks_router
from app.api.worker import router as worker_router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers

app = FastAPI(title=settings.app_name)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(tasks_router)
app.include_router(batches_router)
app.include_router(worker_router)
app.include_router(dashboard_router)


@app.get("/health")
def health():
    return {"status": "ok"}


register_exception_handlers(app)
