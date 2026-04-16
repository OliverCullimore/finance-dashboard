from pydantic import BaseModel


class AssetBase(BaseModel):
    symbol: str = None
    trading212_symbol: str = None
    isin: str = None
    name: str = None
    type: str = None
    current_price: float = None
    currency: str = None
