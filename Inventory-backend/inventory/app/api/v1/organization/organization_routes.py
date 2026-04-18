from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from models.organization import Organization as OrgModel
from pydantic import BaseModel

router = APIRouter(prefix="/organization", tags=["Organization"])

# ---------------- Schemas ----------------
class OrganizationCreate(BaseModel):
    name: str
    businessType: str
    email: str

class OrganizationRead(OrganizationCreate):
    id: str

# ---------------- Routes ----------------

@router.get("/", response_model=OrganizationRead)
def get_organization(db: Session = Depends(get_db)):
    org = db.query(OrgModel).first()
    if not org:
        raise HTTPException(status_code=404, detail="Organization not set")

    return OrganizationRead(
        id=org.id,
        name=org.name,
        businessType=org.business_type,
        email=org.email,
    )


@router.post("/", response_model=OrganizationRead)
def create_organization(org: OrganizationCreate, db: Session = Depends(get_db)):
    existing = db.query(OrgModel).first()
    if existing:
        raise HTTPException(status_code=400, detail="Organization already exists")

    new_org = OrgModel(
        id="org",
        name=org.name,
        business_type=org.businessType,
        email=org.email,
    )
    db.add(new_org)
    db.commit()
    db.refresh(new_org)

    return OrganizationRead(
        id=new_org.id,
        name=new_org.name,
        businessType=new_org.business_type,
        email=new_org.email,
    )


@router.put("/", response_model=OrganizationRead)
def update_organization(org: OrganizationCreate, db: Session = Depends(get_db)):
    existing = db.query(OrgModel).first()
    if not existing:
        raise HTTPException(status_code=404, detail="Organization not set")

    existing.name = org.name
    existing.business_type = org.businessType
    existing.email = org.email
    db.commit()
    db.refresh(existing)

    return OrganizationRead(
        id=existing.id,
        name=existing.name,
        businessType=existing.business_type,
        email=existing.email,
    )
