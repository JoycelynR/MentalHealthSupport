from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from models import Consultation, User, Prescription, Pharmacy, Doctor
from schemas import ConsultationCreate, PrescriptionCreate
from datetime import datetime

router = APIRouter(prefix="/consultations", tags=["Consultations"])


# ---------------------------------------------------
# 1) GET Consultations for Doctor Dashboard
# ---------------------------------------------------
@router.get("/doctor/{doctor_id}")
def get_consultations_for_doctor(doctor_id: int, db: Session = Depends(get_db)):

    consultations = (
        db.query(Consultation)
        .filter(Consultation.doctor_id == doctor_id)
        .options(joinedload(Consultation.user))
        .order_by(Consultation.date.desc())
        .all()
    )

    if not consultations:
        return []  # doctor has no patients yet

    result = []
    for c in consultations:
        result.append({
            "id": c.id,
            "user_id": c.user_id,
            "date": c.date,
            "notes": c.notes,
            "patient_name": c.user.name if c.user else "Unknown",
        })

    return result


# ---------------------------------------------------
# 2) GET Consultations for Patient Dashboard
# ---------------------------------------------------
@router.get("/user/{user_id}")
def get_user_consultations(user_id: int, db: Session = Depends(get_db)):

    consultations = (
        db.query(Consultation)
        .filter(Consultation.user_id == user_id)
        .options(joinedload(Consultation.doctor))
        .order_by(Consultation.date.desc())
        .all()
    )

    if not consultations:
        return []

    results = []
    for c in consultations:
        # Load prescriptions
        pres = db.query(Prescription).filter(
            Prescription.consultation_id == c.id
        ).all()

        pres_list = []
        for p in pres:
            pharmacy = (
                db.query(Pharmacy).filter(Pharmacy.id == p.pharmacy_id).first()
                if p.pharmacy_id else None
            )

            pres_list.append({
                "id": p.id,
                "medication": p.medication,
                "dosage": p.dosage,
                "instructions": p.instructions,
                "pharmacy": {
                    "name": pharmacy.name,
                    "address": pharmacy.address,
                    "contact": pharmacy.contact_number
                } if pharmacy else None
            })

        results.append({
            "id": c.id,
            "date": c.date,
            "doctor_name": c.doctor.name if c.doctor else "Unknown",
            "notes": c.notes,
            "prescriptions": pres_list
        })

    return results


# ---------------------------------------------------
# 3) Update Doctor Notes
# ---------------------------------------------------
@router.put("/{consultation_id}/notes")
def update_notes(consultation_id: int, data: dict, db: Session = Depends(get_db)):

    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id
    ).first()

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    consultation.notes = data.get("notes")
    db.commit()
    db.refresh(consultation)

    return {"message": "Notes updated successfully"}


# ---------------------------------------------------
# 4) Add Prescription
# ---------------------------------------------------
@router.post("/{consultation_id}/prescription")
def add_prescription(
    consultation_id: int,
    data: PrescriptionCreate,
    db: Session = Depends(get_db),
):

    consultation = db.query(Consultation).filter(
        Consultation.id == consultation_id
    ).first()

    if not consultation:
        raise HTTPException(status_code=404, detail="Consultation not found")

    prescription = Prescription(
        consultation_id=consultation_id,
        doctor_id=consultation.doctor_id,
        pharmacy_id=data.pharmacy_id,
        medication=data.medication,
        dosage=data.dosage,
        instructions=data.instructions,
        created_at=datetime.utcnow()
    )

    db.add(prescription)
    db.commit()
    db.refresh(prescription)

    return {"message": "Prescription added", "id": prescription.id}

# ---------------------------------------------------
# 5) Get All Prescriptions For A User (Patient Dashboard)
# ---------------------------------------------------
@router.get("/prescriptions/user/{user_id}")
def get_prescriptions_by_user(user_id: int, db: Session = Depends(get_db)):
    
    # get all consultations for user
    consultations = (
        db.query(Consultation)
        .filter(Consultation.user_id == user_id)
        .all()
    )

    if not consultations:
        return []

    consultation_ids = [c.id for c in consultations]

    # get prescriptions for those consultations
    prescriptions = (
        db.query(Prescription)
        .filter(Prescription.consultation_id.in_(consultation_ids))
        .all()
    )

    result = []
    for p in prescriptions:
        pharmacy = (
            db.query(Pharmacy).filter(Pharmacy.id == p.pharmacy_id).first()
            if p.pharmacy_id else None
        )

        result.append({
            "id": p.id,
            "consultation_id": p.consultation_id,
            "medication": p.medication,
            "dosage": p.dosage,
            "instructions": p.instructions,
            "created_at": p.created_at,
            "pharmacy": {
                "id": pharmacy.id if pharmacy else None,
                "name": pharmacy.name if pharmacy else None,
                "address": pharmacy.address if pharmacy else None,
                "contact": pharmacy.contact_number if pharmacy else None
            }
        })

    return result