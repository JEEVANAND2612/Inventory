from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.models.stock import StockItem
from app.models.stock_history import StockHistory
from app.schemas.stock import StockItemResponse
from app.schemas.stock_history import StockHistoryResponse

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/stock", response_model=List[StockItemResponse])
def stock_report(db: Session = Depends(get_db)):
    return db.query(StockItem).order_by(StockItem.item_name).all()

@router.get("/history", response_model=List[StockHistoryResponse])
def item_wise_history(db: Session = Depends(get_db)):
    return db.query(StockHistory).order_by(
        StockHistory.created_at.desc()
    ).all()

@router.get("/low-stock", response_model=List[StockItemResponse])
def low_stock_report(
    threshold: int = 10,
    db: Session = Depends(get_db)
):
    return (
        db.query(StockItem)
        .filter(StockItem.quantity <= threshold)
        .order_by(StockItem.quantity.asc())
        .all()
    )
