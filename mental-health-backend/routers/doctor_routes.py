from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import doctor_crud
from schemas import DoctorCreate, DoctorResponse

router = APIRouter(prefix="/doctors", tags=["Doctors"])

@router.post("/", response_model=DoctorResponse)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    return doctor_crud.create_doctor(db, doctor)

@router.get("/", response_model=list[DoctorResponse])
def get_doctors(db: Session = Depends(get_db)):
    return doctor_crud.get_doctors(db)

@router.get("/{doctor_id}", response_model=DoctorResponse)
def get_doctor_by_id(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctor_crud.get_doctor_by_id(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@router.delete("/{doctor_id}", response_model=DoctorResponse)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctor_crud.delete_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor
