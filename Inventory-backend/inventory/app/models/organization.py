from sqlalchemy import Column, String
from app.core.database import Base

class Organization(Base):
    __tablename__ = "organization"

    id = Column(String, primary_key=True, index=True, default="org")  # single row
    name = Column(String, nullable=False)
    business_type = Column(String, nullable=False)
    email = Column(String, nullable=False)
