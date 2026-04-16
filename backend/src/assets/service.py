from sqlalchemy import or_

from src.assets.models import Asset
from src.assets.schemas import AssetBase
from src.core.database import db_dependency


class AssetService:
    def __init__(self, db: db_dependency):
        self.db = db

    def get_all(self):
        return self.db.query(Asset).all()

    def get_all_for_sync(self):
        return self.db.query(Asset).filter(or_(Asset.sector_id is None, Asset.industry_id is None)).all()

    def get_by_id(self, asset_id: int):
        return self.db.query(Asset).filter(Asset.id == asset_id).first()

    def get_by_symbol(self, symbol: str):
        return self.db.query(Asset).filter(Asset.symbol == symbol).first()

    def get_by_isin(self, isin: str):
        return self.db.query(Asset).filter(Asset.isin == isin).first()

    def upsert(self, data: AssetBase):
        asset = self.db.query(Asset).filter(
            Asset.isin == data.isin,
            Asset.type == data.type
        ).first()

        if asset:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(asset, field, value)
        else:
            asset = Asset(**data.model_dump())
            self.db.add(asset)

        self.db.commit()
        self.db.refresh(asset)
        return asset

    def delete(self, asset_id: int):
        asset = self.get_by_id(asset_id)

        if not asset:
            return False

        self.db.delete(asset)
        self.db.commit()
        return True
