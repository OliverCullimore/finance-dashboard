import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func

from src.core.database import Base
from src.core.utils import CurrencyEnum


class TransactionType(enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRADE = "trade"
    DIVIDEND = "dividend"
    FEE = "fee"
    TRANSFER = "transfer"


# Transaction type enum
TransactionTypeEnum = Enum(TransactionType, name="transaction_type")


class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    external_id = Column(String, nullable=False)
    type = Column(TransactionTypeEnum, nullable=False)
    amount = Column(Float, default=0, nullable=False)
    currency = Column(CurrencyEnum, nullable=False)
    description = Column(Text)
    asset_id = Column(Integer, ForeignKey("assets.id"))
    quantity = Column(Float)
    price = Column(Float)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("account_id", "external_id"),
    )
