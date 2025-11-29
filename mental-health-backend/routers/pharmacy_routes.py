from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import pharmacy_crud
from schemas import PharmacyCreate, PharmacyResponse

router = APIRouter(prefix="/pharmacies", tags=["Pharmacies"])

@router.post("/", response_model=PharmacyResponse)
def create_pharmacy(pharmacy: PharmacyCreate, db: Session = Depends(get_db)):
    return pharmacy_crud.create_pharmacy(db, pharmacy)

@router.get("/", response_model=list[PharmacyResponse])
def get_pharmacies(db: Session = Depends(get_db)):
    return pharmacy_crud.get_pharmacies(db)

@router.get("/{pharmacy_id}", response_model=PharmacyResponse)
def get_pharmacy_by_id(pharmacy_id: int, db: Session = Depends(get_db)):
    pharmacy = pharmacy_crud.get_pharmacy_by_id(db, pharmacy_id)
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")
    return pharmacy

@router.delete("/{pharmacy_id}", response_model=PharmacyResponse)
def delete_pharmacy(pharmacy_id: int, db: Session = Depends(get_db)):
    pharmacy = pharmacy_crud.delete_pharmacy(db, pharmacy_id)
    if not pharmacy:
        raise HTTPException(status_code=404, detail="Pharmacy not found")
    return pharmacy
