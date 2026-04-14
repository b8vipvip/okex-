from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.core.response import err


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(HTTPException)
    async def http_exc_handler(_: Request, exc: HTTPException):
        return JSONResponse(status_code=exc.status_code, content=err(exc.status_code, str(exc.detail)))

    @app.exception_handler(ValidationError)
    async def validation_exc_handler(_: Request, exc: ValidationError):
        return JSONResponse(status_code=422, content=err(4001, "invalid params", exc.errors()))

    @app.exception_handler(Exception)
    async def unhandled_exc_handler(_: Request, exc: Exception):
        return JSONResponse(status_code=500, content=err(5000, f"internal error: {exc}"))
