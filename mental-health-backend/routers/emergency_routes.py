from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from crud import emergency_crud
from schemas import EmergencyCreate, EmergencyResponse

router = APIRouter(prefix="/emergencies", tags=["Emergencies"])

@router.post("/", response_model=EmergencyResponse)
def create_emergency(emergency: EmergencyCreate, db: Session = Depends(get_db)):
    return emergency_crud.create_emergency(db, emergency)

@router.get("/", response_model=list[EmergencyResponse])
def get_emergencies(db: Session = Depends(get_db)):
    return emergency_crud.get_emergencies(db)

@router.put("/{emergency_id}/status", response_model=EmergencyResponse)
def update_status(emergency_id: int, new_status: str, db: Session = Depends(get_db)):
    emergency = emergency_crud.update_emergency_status(db, emergency_id, new_status)
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")
    return emergency

@router.delete("/{emergency_id}", response_model=EmergencyResponse)
def delete_emergency(emergency_id: int, db: Session = Depends(get_db)):
    emergency = emergency_crud.delete_emergency(db, emergency_id)
    if not emergency:
        raise HTTPException(status_code=404, detail="Emergency not found")
    return emergency
