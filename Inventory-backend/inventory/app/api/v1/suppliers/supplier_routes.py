from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.api.v1.suppliers.supplier_schemas import SupplierCreate, SupplierUpdate, SupplierOut
from app.api.v1.suppliers.supplier_service import (
    get_all_suppliers,
    get_supplier,
    create_supplier as service_create_supplier,
    update_supplier as service_update_supplier,
    delete_supplier as service_delete_supplier,
)

router = APIRouter(prefix="/suppliers", tags=["Suppliers"])

@router.get("/", response_model=List[SupplierOut])
def read_suppliers(db: Session = Depends(get_db)):
    return get_all_suppliers(db)

@router.post("/", response_model=SupplierOut)
def create_supplier(supplier: SupplierCreate, db: Session = Depends(get_db)):
    return service_create_supplier(db, supplier)

@router.put("/{supplier_id}", response_model=SupplierOut)
def update_supplier(supplier_id: int, updates: SupplierUpdate, db: Session = Depends(get_db)):
    updated = service_update_supplier(db, supplier_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return updated

@router.delete("/{supplier_id}")
def delete_supplier(supplier_id: int, db: Session = Depends(get_db)):
    deleted = service_delete_supplier(db, supplier_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Supplier not found")
    return {"detail": "Supplier deleted successfully"}
