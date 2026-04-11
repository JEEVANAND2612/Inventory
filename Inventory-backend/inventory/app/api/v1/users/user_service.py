from sqlalchemy.orm import Session
from app.models.user import User
from app.core.security import hash_password
from .user_schemas import UserCreate, UserUpdate


def create_user(db: Session, user_in: UserCreate) -> User:
    user = User(
        email=user_in.email,
        name=user_in.name,
        hashed_password=hash_password(user_in.password),
        role=user_in.role or "Staff",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def update_user(db: Session, user_id: int, user_in: UserUpdate) -> User:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        return None

    for key, value in user_in.dict(exclude_unset=True).items():
        setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user
