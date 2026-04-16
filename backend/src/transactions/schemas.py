from datetime import datetime

from pydantic import BaseModel


class TransactionBase(BaseModel):
    external_id: str = None
    type: str = None
    amount: float = None
    currency: str = None
    description: str | None = None
    asset_id: int | None = None
    quantity: float | None = None
    price: float | None = None
    created_at: datetime = None


class TransactionResponse(TransactionBase):
    id: int
    account_id: int = None
    created_at: datetime
    updated_at: datetime = None


class PositionBase(BaseModel):
    asset_id: int = None
    quantity: float = None
    avg_price: float = None
