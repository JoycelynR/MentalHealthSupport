from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Doctor, Consultation, Pharmacy

router = APIRouter(prefix="/admin", tags=["Admin"])

@router.get("/dashboard")
def admin_dashboard(db: Session = Depends(get_db)):
    users = db.query(User).count()
    doctors = db.query(Doctor).count()
    consultations = db.query(Consultation).count()
    pharmacies = db.query(Pharmacy).count()

    return {
        "users_count": users,
        "doctors_count": doctors,
        "consultations_count": consultations,
        "pharmacy_count": pharmacies
    }
