from sqlalchemy.orm import Session
from models import Pharmacy
from schemas import PharmacyCreate

def create_pharmacy(db: Session, pharmacy: PharmacyCreate):
    new_pharmacy = Pharmacy(
        name=pharmacy.name,
        address=pharmacy.address,
        contact=pharmacy.contact
    )
    db.add(new_pharmacy)
    db.commit()
    db.refresh(new_pharmacy)
    return new_pharmacy

def get_pharmacies(db: Session):
    return db.query(Pharmacy).all()

def get_pharmacy_by_id(db: Session, pharmacy_id: int):
    return db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()

def delete_pharmacy(db: Session, pharmacy_id: int):
    pharmacy = db.query(Pharmacy).filter(Pharmacy.id == pharmacy_id).first()
    if pharmacy:
        db.delete(pharmacy)
        db.commit()
    return pharmacy
