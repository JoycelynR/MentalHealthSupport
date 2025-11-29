from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import User, Doctor
from schemas import UserCreate
from auth_utils import verify_password, create_access_token, hash_password

router = APIRouter(prefix="/users", tags=["Users"])

# -------------------------------------------------
# LOGIN (Patients/Admins from User table, Doctors from Doctor table)
# -------------------------------------------------
@router.post("/login")
def login(email: str, password: str, role: str, db: Session = Depends(get_db)):

    # -----------------------------
    # PATIENT or ADMIN LOGIN
    # -----------------------------
    if role.lower() != "doctor":
        user = db.query(User).filter(
            User.email == email,
            User.role == role.lower()
        ).first()

        if not user:
            raise HTTPException(status_code=401, detail="User with this role not found")

        if not verify_password(password, user.password):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        token = create_access_token({"sub": user.email, "role": user.role})

        return {
            "access_token": token,
            "token_type": "bearer",
            "role": user.role,
            "user_id": user.id,
            "doctor_id": None,
            "name": user.name,
            "email": user.email
        }

    # -----------------------------
    # DOCTOR LOGIN (From Doctor Table)
    # -----------------------------
    doctor = db.query(Doctor).filter(Doctor.email == email).first()

    if not doctor:
        raise HTTPException(status_code=401, detail="Doctor not found")

    if not verify_password(password, doctor.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": doctor.email, "role": "doctor"})

    return {
        "access_token": token,
        "token_type": "bearer",
        "role": "doctor",
        "user_id": None,
        "doctor_id": doctor.id,         # ⭐ FIXED
        "name": doctor.name,
        "email": doctor.email
    }


# -------------------------------------------------
# REGISTER (Patients only)
# -------------------------------------------------
@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(
        name=user.name,
        email=user.email,
        password=hash_password(user.password),
        role="patient"            # force patient registration
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Patient registered successfully", "user_id": new_user.id}
