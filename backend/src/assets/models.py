import enum

from sqlalchemy import Column, DateTime, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.sql import func

from src.core.database import Base
from src.core.utils import CurrencyEnum


class AssetType(enum.Enum):
    STOCK = "stock"
    ETF = "etf"
    CRYPTO = "crypto"


# Asset type enum
AssetTypeEnum = Enum(AssetType, name="asset_type")


class Asset(Base):
    __tablename__ = "assets"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, nullable=False)
    isin = Column(String, nullable=False)
    name = Column(String, nullable=False)
    type = Column(AssetTypeEnum, nullable=False)
    current_price = Column(Float, nullable=False)
    currency = Column(CurrencyEnum, nullable=False)
    sector_id = Column(Integer, ForeignKey("sectors.id"))
    industry_id = Column(Integer, ForeignKey("industries.id"))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())
