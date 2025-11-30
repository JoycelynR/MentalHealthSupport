from sqlalchemy.orm import Session
from models import Doctor, User
from schemas import DoctorCreate

def create_doctor(db: Session, doctor: DoctorCreate):
    # 1. Create a user row
    user = User(
        name=doctor.name,
        email=doctor.email,
        password=doctor.password,   # hash later
        role="doctor"
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    # 2. Create doctor row linked to user
    new_doctor = Doctor(
        name=doctor.name,
        email=doctor.email,
        password=doctor.password,
        role="doctor",
        contact_number=doctor.contact_number,
        license_no=doctor.license_no
    )
    db.add(new_doctor)
    db.commit()
    db.refresh(new_doctor)

    return new_doctor

def get_doctors(db: Session):
    return db.query(Doctor).all()

def get_doctor_by_id(db: Session, doctor_id: int):
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()

def delete_doctor(db: Session, doctor_id: int):
    doctor = db.query(Doctor).filter(Doctor.id == doctor_id).first()
    if doctor:
        db.delete(doctor)
        db.commit()
    return doctor
