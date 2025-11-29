from sqlalchemy.orm import Session
from models import Consultation
from schemas import ConsultationCreate

def create_consultation(db: Session, consultation: ConsultationCreate):
    new_consult = Consultation(
        doctor_id=consultation.doctor_id,
        patient_id=consultation.patient_id,
        assessment_id=consultation.assessment_id,
        notes=consultation.notes
    )
    db.add(new_consult)
    db.commit()
    db.refresh(new_consult)
    return new_consult

def get_consultations(db: Session):
    return db.query(Consultation).all()

def get_consultation_by_id(db: Session, consultation_id: int):
    return db.query(Consultation).filter(Consultation.id == consultation_id).first()

def delete_consultation(db: Session, consultation_id: int):
    consultation = db.query(Consultation).filter(Consultation.id == consultation_id).first()
    if consultation:
        db.delete(consultation)
        db.commit()
    return consultation
