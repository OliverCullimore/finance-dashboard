from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AccountBase(BaseModel):
    connection_id: int | None = None
    source: str
    external_id: str
    name: str
    description: str
    balance: float
    currency: str = "GBP"


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    balance: Optional[float] = None
    currency: Optional[str] = None


class AccountResponse(AccountBase):
    id: int
    created_at: datetime
    updated_at: datetime = None
