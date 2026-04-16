from src.categories.models import Category
from src.categories.schemas import CategoryBase
from src.core.database import db_dependency


class CategoryService:
    def __init__(self, db: db_dependency):
        self.db = db

    def get_all(self):
        return self.db.query(Category).all()

    def get_by_id(self, category_id: int):
        return self.db.query(Category).filter(Category.id == category_id).first()

    def get_by_name(self, category_name: str):
        return self.db.query(Category).filter(Category.name == category_name).first()

    def upsert(self, data: CategoryBase):
        category = self.get_by_name(data.name)

        if category:
            for field, value in data.model_dump(exclude_unset=True).items():
                setattr(category, field, value)
        else:
            category = Category(**data.model_dump())
            self.db.add(category)

        self.db.commit()
        self.db.refresh(category)
        return category

    def delete(self, category_id: int):
        category = self.get_by_id(category_id)

        if not category:
            return False

        self.db.delete(category)
        self.db.commit()
        return True
