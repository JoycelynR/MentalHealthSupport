from sqlalchemy.orm import Session
from models import Emergency
from schemas import EmergencyCreate

def create_emergency(db: Session, emergency: EmergencyCreate):
    new_emergency = Emergency(
        user_id=emergency.user_id,
        message=emergency.message,
        status="Pending"
    )
    db.add(new_emergency)
    db.commit()
    db.refresh(new_emergency)
    return new_emergency

def get_emergencies(db: Session):
    return db.query(Emergency).all()

def update_emergency_status(db: Session, emergency_id: int, new_status: str):
    emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
    if emergency:
        emergency.status = new_status
        db.commit()
        db.refresh(emergency)
    return emergency

def delete_emergency(db: Session, emergency_id: int):
    emergency = db.query(Emergency).filter(Emergency.id == emergency_id).first()
    if emergency:
        db.delete(emergency)
        db.commit()
    return emergency
