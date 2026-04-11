from pydantic import BaseModel

class WarehouseCreate(BaseModel):
    id: str
    name: str
    location: str

class WarehouseRead(WarehouseCreate):
    pass
