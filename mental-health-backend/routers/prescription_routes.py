from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import prescription_crud
from schemas import PrescriptionCreate, PrescriptionResponse
from dependencies import get_current_user  

router = APIRouter(prefix="/prescriptions", tags=["Prescriptions"])


@router.post("/", response_model=PrescriptionResponse)
def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Only doctors can create prescriptions
    if current_user.role != "doctor":
        raise HTTPException(status_code=403, detail="Only doctors can prescribe.")
    return prescription_crud.create_prescription(db, prescription)


@router.get("/", response_model=list[PrescriptionResponse])
def get_prescriptions(
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Only doctors or admins can view all prescriptions
    if current_user.role not in ["doctor", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied.")
    return prescription_crud.get_prescriptions(db)


@router.get("/{prescription_id}", response_model=PrescriptionResponse)
def get_prescription_by_id(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Doctors and Admins can access individual prescriptions
    if current_user.role not in ["doctor", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied.")

    pres = prescription_crud.get_prescription_by_id(db, prescription_id)
    if not pres:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return pres


@router.delete("/{prescription_id}", response_model=PrescriptionResponse)
def delete_prescription(
    prescription_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    # Only doctors and admins can delete prescriptions
    if current_user.role not in ["doctor", "admin"]:
        raise HTTPException(status_code=403, detail="Access denied.")

    pres = prescription_crud.delete_prescription(db, prescription_id)
    if not pres:
        raise HTTPException(status_code=404, detail="Prescription not found")
    return pres
