from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ConnectionBase(BaseModel):
    provider: str


class ConnectionUpsert(ConnectionBase):
    api_key: Optional[str] = None
    api_secret: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    status: Optional[str] = None


class ConnectionResponse(ConnectionBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime = None
