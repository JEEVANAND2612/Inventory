from pydantic import BaseModel
from datetime import datetime

class StockHistoryResponse(BaseModel):
    id: int
    stock_item_id: int
    item_name: str
    quantity_change: int
    price: float
    action: str
    created_at: datetime

    class Config:
        from_attributes = True
