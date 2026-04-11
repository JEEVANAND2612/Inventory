from pydantic import BaseModel
from typing import Optional


class WarehouseBase(BaseModel):
    name: str
    location: str


class WarehouseCreate(WarehouseBase):
    """Used for CREATE – no id"""
    pass


class WarehouseUpdate(WarehouseBase):
    """Used for UPDATE – no id in body"""
    pass


class WarehouseRead(WarehouseBase):
    id: str

    class Config:
        from_attributes = True  # pydantic v2 (orm_mode replacement)
