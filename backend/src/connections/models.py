from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.sql import func

from src.core.database import Base
from src.core.utils import SourceEnum


class Connection(Base):
    __tablename__ = "connections"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    provider = Column(SourceEnum, nullable=False)
    api_key = Column(String)
    api_secret = Column(String)
    access_token = Column(String)
    refresh_token = Column(String)
    status = Column(String, default="unknown")
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
