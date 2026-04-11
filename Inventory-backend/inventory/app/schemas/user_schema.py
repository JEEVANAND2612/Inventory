from pydantic import BaseModel

class UserCreate(BaseModel):
    email: str
    name: str
    password: str
    role: str
    employee_id: str  # <- required

class UserRead(UserCreate):
    pass
