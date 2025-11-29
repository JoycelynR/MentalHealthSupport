from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import User, Doctor
from utils import create_access_token
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["Authentication"])

class LoginRequest(BaseModel):
    email: str
    password: str
    role: str


@router.post("/login")
def login_user(request: LoginRequest, db: Session = Depends(get_db)):
    # Check which table to look in based on role
    if request.role.lower() == "doctor":
        user = db.query(Doctor).filter(Doctor.email == request.email).first()
    else:
        user = db.query(User).filter(User.email == request.email).first()

    # Validate user existence
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Compare password directly (since we removed hashing)
    if user.password != request.password:
        raise HTTPException(status_code=401, detail="Invalid password")

    # Validate role correctness
    if getattr(user, "role", "doctor").lower() != request.role.lower():
        raise HTTPException(status_code=403, detail=f"User is not registered as {request.role}")

    # Generate token
    token = create_access_token({"sub": user.email, "role": request.role})
    return {"access_token": token, "token_type": "bearer", "role": request.role,"user_id": user.id}
