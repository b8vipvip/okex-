from fastapi import APIRouter, HTTPException

from app.core.response import ok
from app.core.security import create_access_token, verify_login
from app.schemas.auth import LoginIn

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/login")
def login(payload: LoginIn):
    if not verify_login(payload.username, payload.password):
        raise HTTPException(status_code=401, detail="username or password invalid")
    token = create_access_token(payload.username)
    return ok({"token": token, "token_type": "Bearer"})
