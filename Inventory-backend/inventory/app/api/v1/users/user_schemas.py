from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    employee_id: str
    email: EmailStr
    name: str
    password: str
    role: Optional[str] = "Staff"


class UserUpdate(BaseModel):
    employee_id: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None


class UserRead(BaseModel):
    id: int
    employee_id: str
    email: EmailStr
    name: str
    role: str

    class Config:
        from_attributes = True