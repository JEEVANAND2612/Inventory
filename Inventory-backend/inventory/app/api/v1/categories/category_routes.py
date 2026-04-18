from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from api.deps import get_db
from api.v1.categories import category_service
from api.v1.categories.category_schemas import (
    CategoryCreate,
    CategoryUpdate,
    CategoryOut,
)
from models.category import Category

router = APIRouter(
    prefix="/categories",
    tags=["Categories"],
)

@router.get("/", response_model=List[CategoryOut])
def get_categories(db: Session = Depends(get_db)):
    return category_service.get_categories(db)


@router.post("/", response_model=CategoryOut, status_code=status.HTTP_201_CREATED)
def create_category(
    data: CategoryCreate,
    db: Session = Depends(get_db),
):
    existing = db.query(Category).filter(
        Category.name == data.name
    ).first()

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Category already exists",
        )

    return category_service.create_category(db, data)


@router.put("/{category_id}", response_model=CategoryOut)
def update_category(
    category_id: int,
    data: CategoryUpdate,
    db: Session = Depends(get_db),
):
    category = category_service.update_category(db, category_id, data)

    if not category:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    return category


@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
):
    success = category_service.delete_category(db, category_id)

    if not success:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )
