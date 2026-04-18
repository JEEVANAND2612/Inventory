import uuid
from sqlalchemy import Column, String
from core.database import Base

class Warehouse(Base):
    __tablename__ = "warehouses"

    id = Column(String, primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    location = Column(String, nullable=False)
