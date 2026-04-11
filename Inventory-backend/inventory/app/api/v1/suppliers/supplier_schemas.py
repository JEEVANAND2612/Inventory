from pydantic import BaseModel
from typing import Optional

class SupplierCreate(BaseModel):
    name: str
    contact_name: str
    phone: str
    email: str
    items: str
    attachment: Optional[str] = None

class SupplierUpdate(BaseModel):
    name: Optional[str] = None
    contact_name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    items: Optional[str] = None
    attachment: Optional[str] = None

class SupplierOut(BaseModel):
    id: int
    name: str
    contact_name: str
    phone: str
    email: str
    items: str
    attachment: Optional[str] = None

    class Config:
        from_attributes = True
