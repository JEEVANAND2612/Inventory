from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from core.database import get_db
from models.stock import StockItem
from models.stock_history import StockHistory
from schemas.stock import StockItemCreate, StockItemUpdate, StockItemResponse

router = APIRouter(prefix="/stock", tags=["Stock"])

@router.get("/", response_model=List[StockItemResponse])
def list_stock(db: Session = Depends(get_db)):
    return db.query(StockItem).order_by(StockItem.id.desc()).all()

@router.post("/", response_model=StockItemResponse)
def add_stock(data: StockItemCreate, db: Session = Depends(get_db)):
    item = StockItem(**data.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)

    # Store history
    history = StockHistory(
        stock_item_id=item.id,
        item_name=item.item_name,
        quantity_change=item.quantity,
        price=item.price,
        action="CREATED"
    )
    db.add(history)
    db.commit()

    return item

@router.put("/{item_id}", response_model=StockItemResponse)
def update_stock(item_id: int, data: StockItemUpdate, db: Session = Depends(get_db)):
    item = db.query(StockItem).filter(StockItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Stock item not found")

    old_quantity = item.quantity
    for field, value in data.model_dump(exclude_unset=True).items():
        setattr(item, field, value)

    db.commit()
    db.refresh(item)

    # Store history
    quantity_diff = item.quantity - old_quantity
    history = StockHistory(
        stock_item_id=item.id,
        item_name=item.item_name,
        quantity_change=quantity_diff,
        price=item.price,
        action="UPDATED"
    )
    db.add(history)
    db.commit()

    return item

@router.delete("/{item_id}", status_code=204)
def delete_stock(item_id: int, db: Session = Depends(get_db)):
    item = db.query(StockItem).filter(StockItem.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Stock item not found")

    db.delete(item)
    db.commit()
    return None
