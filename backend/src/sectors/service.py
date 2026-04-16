from src.core.database import db_dependency
from src.sectors.models import Sector
from src.sectors.schemas import SectorBase


class SectorService:
    def __init__(self, db: db_dependency):
        self.db = db

    def get_all(self):
        return self.db.query(Sector).all()

    def get_by_id(self, sector_id: int):
        return self.db.query(Sector).filter(Sector.id == sector_id).first()

    def get_by_name(self, sector_name: str):
        return self.db.query(Sector).filter(Sector.name == sector_name).first()

    def upsert(self, data: SectorBase):
        sector = self.get_by_name(data.name)

        if sector:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(sector, field, value)
        else:
            sector = Sector(**data.model_dump())
            self.db.add(sector)

        self.db.commit()
        self.db.refresh(sector)
        return sector

    def delete(self, sector_id: int):
        sector = self.get_by_id(sector_id)

        if not sector:
            return False

        self.db.delete(sector)
        self.db.commit()
        return True
