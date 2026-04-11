from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.v1.warehouses import warehouse_service
from app.api.v1.warehouses.warehouse_schemas import (
    WarehouseCreate,
    WarehouseUpdate,
    WarehouseRead,
)

router = APIRouter(prefix="/warehouses", tags=["Warehouses"])


@router.get("/", response_model=List[WarehouseRead])
def get_warehouses(db: Session = Depends(get_db)):
    return warehouse_service.get_all_warehouses(db)


@router.post("/", response_model=WarehouseRead)
def create_warehouse(
    warehouse: WarehouseCreate,
    db: Session = Depends(get_db),
):
    return warehouse_service.create_warehouse(db, warehouse)


@router.put("/{warehouse_id}", response_model=WarehouseRead)
def update_warehouse(
    warehouse_id: str,
    warehouse: WarehouseUpdate,
    db: Session = Depends(get_db),
):
    updated = warehouse_service.update_warehouse(
        db, warehouse_id, warehouse
    )

    if not updated:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    return updated


@router.delete("/{warehouse_id}")
def delete_warehouse(
    warehouse_id: str,
    db: Session = Depends(get_db),
):
    deleted = warehouse_service.delete_warehouse(db, warehouse_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Warehouse not found")

    return {"detail": "Warehouse deleted"}
