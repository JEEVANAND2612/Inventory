from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True)
    description = Column(String, nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    stock_items = relationship(
        "StockItem",
        back_populates="category",
        cascade="all, delete-orphan"
    )
