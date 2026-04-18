from fastapi import APIRouter, HTTPException, Depends, status, Response, Request
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from uuid import uuid4


from api.deps import get_db , get_current_user
from models.user import User
from api.v1.auth.auth_schemas import SignupRequest, LoginRequest
from api.v1.auth.auth_service import (
    hash_password,
    verify_password,
    create_access_token,
)
from core.config import settings

router = APIRouter(prefix="/auth", tags=["Auth"])
COOKIE_NAME = "access_token"


# =========================
# Signup
# =========================

@router.post("/signup", status_code=status.HTTP_201_CREATED)
def signup(data: SignupRequest, db: Session = Depends(get_db)):
    
    existing_user = db.query(User).filter(User.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    print("kjdfdjfbndkfjdbnfkb")
    # Generate a unique employee_id
    employee_id = str(uuid4())

    user = User(
        name=data.name,
        email=data.email,
        hashed_password=hash_password(data.password),
        employee_id=employee_id  # <-- must set this!
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    print("mai gvhdfjdbfjdvjbfjdjf")
    return {"message": "User created successfully", "employee_id": employee_id}


# =========================
# Login
# =========================
@router.post("/login")
def login(
    data: LoginRequest,
    response: Response,
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == data.email).first()

    if not user or not verify_password(
        data.password,
        user.hashed_password,
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token({"sub": user.email})

    response.set_cookie(
        key=COOKIE_NAME,
        value=token,
        httponly=True,
        samesite="lax",
        secure=False,   # ⚠️ set True in production (HTTPS)
        max_age=60 * 30,
    )

    return {"message": "Login successful"}


# =========================
# Get Current User
# =========================
@router.get("/me")
def get_me(
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
    }


# =========================
# Logout
# =========================
@router.post("/logout")
def logout(response: Response):
    response.delete_cookie(COOKIE_NAME)
    return {"message": "Logged out successfully"}
