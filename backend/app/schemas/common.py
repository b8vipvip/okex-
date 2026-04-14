from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class APIResponse(BaseModel):
    code: int = 0
    message: str = "success"
    data: dict | list | None = None


class PageResult(BaseModel):
    total: int
    page: int
    page_size: int
    items: list


class ORMBase(BaseModel):
    model_config = ConfigDict(from_attributes=True, json_encoders={Decimal: lambda v: format(v, ".2f"), datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S") if v else None})
