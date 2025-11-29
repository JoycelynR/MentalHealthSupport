from sqlalchemy.orm import Session
from models import Prescription
from schemas import PrescriptionCreate

def create_prescription(db: Session, prescription: PrescriptionCreate):
    new_pres = Prescription(
        consultation_id=prescription.consultation_id,
        medicine_name=prescription.medicine_name,
        dosage=prescription.dosage,
        instructions=prescription.instructions,
        pharmacy_id=prescription.pharmacy_id
    )
    db.add(new_pres)
    db.commit()
    db.refresh(new_pres)
    return new_pres

def get_prescriptions(db: Session):
    return db.query(Prescription).all()

def get_prescription_by_id(db: Session, prescription_id: int):
    return db.query(Prescription).filter(Prescription.id == prescription_id).first()

def delete_prescription(db: Session, prescription_id: int):
    pres = db.query(Prescription).filter(Prescription.id == prescription_id).first()
    if pres:
        db.delete(pres)
        db.commit()
    return pres
