from pydantic import BaseModel

class OrganizationCreate(BaseModel):
    name: str
    businessType: str
    email: str

class OrganizationRead(OrganizationCreate):
    id: str
