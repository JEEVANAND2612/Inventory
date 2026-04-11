from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.user import User as UserModel
from app.core.security import hash_password
from .user_schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", response_model=List[UserRead])
def get_users(db: Session = Depends(get_db)):
    return db.query(UserModel).all()
@router.post("/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    existing_user = (
        db.query(UserModel)
        .filter(UserModel.employee_id == user.employee_id)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists"
        )

    db_user = UserModel(
        employee_id=user.employee_id,
        email=user.email,
        name=user.name,
        hashed_password=hash_password(user.password),
        role=user.role,
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception:
        db.rollback()
        raise


@router.put("/{user_id}", response_model=UserRead)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):

    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()

    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    # Employee ID uniqueness check
    if user.employee_id:
        existing_user = (
            db.query(UserModel)
            .filter(
                UserModel.employee_id == user.employee_id,
                UserModel.id != user_id
            )
            .first()
        )

        if existing_user:
            raise HTTPException(
                status_code=400,
                detail="Employee ID already exists"
            )

        db_user.employee_id = user.employee_id

    if user.email:
        db_user.email = user.email

    if user.name:
        db_user.name = user.name

    if user.role:
        db_user.role = user.role

    # Update password only if provided
    if user.password:
        db_user.hashed_password = hash_password(user.password)

    try:
        db.commit()
        db.refresh(db_user)
        return db_user

    except Exception:
        db.rollback()
        raise

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(db_user)
    db.commit()
    return {"detail": "User deleted"}
