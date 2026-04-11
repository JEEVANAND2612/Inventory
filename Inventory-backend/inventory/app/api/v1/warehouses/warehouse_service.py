from sqlalchemy.orm import Session
from app.models.warehouse import Warehouse as WarehouseModel
from app.api.v1.warehouses.warehouse_schemas import (
    WarehouseCreate,
    WarehouseUpdate,
)


def get_all_warehouses(db: Session):
    return db.query(WarehouseModel).all()


def create_warehouse(db: Session, warehouse: WarehouseCreate):
    db_warehouse = WarehouseModel(
        name=warehouse.name,
        location=warehouse.location,
    )
    db.add(db_warehouse)
    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse


def update_warehouse(db: Session, warehouse_id: str, warehouse: WarehouseUpdate):
    db_warehouse = (
        db.query(WarehouseModel)
        .filter(WarehouseModel.id == warehouse_id)
        .first()
    )

    if not db_warehouse:
        return None

    db_warehouse.name = warehouse.name
    db_warehouse.location = warehouse.location

    db.commit()
    db.refresh(db_warehouse)
    return db_warehouse


def delete_warehouse(db: Session, warehouse_id: str) -> bool:
    db_warehouse = (
        db.query(WarehouseModel)
        .filter(WarehouseModel.id == warehouse_id)
        .first()
    )

    if not db_warehouse:
        return False

    db.delete(db_warehouse)
    db.commit()
    return True
