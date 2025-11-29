from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session


from database import get_db
from models import User
from schemas import UserCreate, UserResponse


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register")
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Register a new user (doctor, patient, or admin)."""
    valid_roles = ["patient", "doctor", "admin"]
    if user.role.lower() not in valid_roles:
        raise HTTPException(status_code=400, detail="Invalid role")

    # Check for duplicates
    existing_user = db.query(User).filter(User.email == user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    db_user = User(
        name=user.name,
        email=user.email,
        password=user.password,
        role=user.role.lower(),
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return {"message": f"{user.role.capitalize()} registered successfully!", "user_id": db_user.id}
