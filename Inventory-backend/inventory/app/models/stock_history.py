from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.sql import func
from core.database import Base

class StockHistory(Base):
    __tablename__ = "stock_history"

    id = Column(Integer, primary_key=True, index=True)
    stock_item_id = Column(Integer, nullable=False)
    item_name = Column(String, nullable=False)
    quantity_change = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    action = Column(String, nullable=False)  # CREATED / UPDATED / DELETED
    created_at = Column(DateTime(timezone=True), server_default=func.now())
