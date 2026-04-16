from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.sql import func

from src.core.database import Base
from src.core.utils import CurrencyEnum, SourceEnum


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    connection_id = Column(Integer, ForeignKey("connections.id"), nullable=True)
    source = Column(SourceEnum, nullable=False)
    external_id = Column(String, nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    balance = Column(Float, default=0, nullable=False)
    currency = Column(CurrencyEnum, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    __table_args__ = (
        UniqueConstraint("user_id", "source", "external_id"),
    )
