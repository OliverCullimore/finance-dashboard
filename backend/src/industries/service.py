from src.core.database import db_dependency
from src.industries.models import Industry
from src.industries.schemas import IndustryBase


class IndustryService:
    def __init__(self, db: db_dependency):
        self.db = db

    def get_all(self):
        return self.db.query(Industry).all()

    def get_by_id(self, industry_id: int):
        return self.db.query(Industry).filter(Industry.id == industry_id).first()

    def get_by_name(self, industry_name: str):
        return self.db.query(Industry).filter(Industry.name == industry_name).first()

    def upsert(self, data: IndustryBase):
        industry = self.get_by_name(data.name)

        if industry:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(industry, field, value)
        else:
            industry = Industry(**data.model_dump())
            self.db.add(industry)

        self.db.commit()
        self.db.refresh(industry)
        return industry

    def delete(self, industry_id: int):
        industry = self.get_by_id(industry_id)

        if not industry:
            return False

        self.db.delete(industry)
        self.db.commit()
        return True
