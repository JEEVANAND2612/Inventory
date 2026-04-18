from sqlalchemy.orm import Session
from models.category import Category
from api.v1.categories.category_schemas import (
    CategoryCreate,
    CategoryUpdate,
)

def get_categories(db: Session):
    return db.query(Category).order_by(Category.id.desc()).all()


def create_category(db: Session, data: CategoryCreate):
    category = Category(
        name=data.name,
        description=data.description,
    )
    db.add(category)
    db.commit()
    db.refresh(category)
    return category


def update_category(db: Session, category_id: int, data: CategoryUpdate):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return None

    category.name = data.name
    category.description = data.description
    db.commit()
    db.refresh(category)
    return category


def delete_category(db: Session, category_id: int):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        return False

    db.delete(category)
    db.commit()
    return True
