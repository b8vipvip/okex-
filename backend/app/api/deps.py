from fastapi import Depends

from app.core.security import admin_auth, worker_auth

AdminUser = Depends(admin_auth)
WorkerAuth = Depends(worker_auth)
