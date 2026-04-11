from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class StockItemBase(BaseModel):
    item_name: str
    category_id: int
    quantity: int
    price: float

class StockItemCreate(StockItemBase):
    pass

class StockItemUpdate(BaseModel):
    quantity: Optional[int] = None
    price: Optional[float] = None

class StockItemResponse(StockItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
