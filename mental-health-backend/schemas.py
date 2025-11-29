from pydantic import BaseModel
from datetime import datetime
from typing import Optional


# USER SCHEMAS

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    role: str  # "patient", "doctor", "admin"


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    class Config:
        from_attributes = True  # replaces orm_mode in Pydantic v2


# ASSESSMENT SCHEMAS

class AssessmentCreate(BaseModel):
    user_id: int
    mood_score: int


class AssessmentResponse(BaseModel):
    id: int
    user_id: int
    mood_score: int
    recommendation: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True



# DOCTOR SCHEMAS
class DoctorCreate(BaseModel):
    name: str
    email: str
    password: str
    contact_number: str | None = None
    license_no: str | None = None
    
class DoctorResponse(BaseModel):
    id: int
    name: str
    email: str
    contact_number: str | None = None
    license_no: str | None = None

    class Config:
        from_attributes = True




# CONSULTATION SCHEMAS

class ConsultationCreate(BaseModel):
    doctor_id: int
    patient_id: int
    assessment_id: int
    notes: str


class ConsultationResponse(BaseModel):
    id: int
    doctor_id: int
    patient_id: int
    assessment_id: int
    notes: str
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True



# PRESCRIPTION SCHEMAS

class PrescriptionCreate(BaseModel):
    consultation_id: int
    medication: str
    dosage: str
    instructions: str
    pharmacy_id: int | None = None 


class PrescriptionResponse(BaseModel):
    id: int
    consultation_id: int
    medicine_name: str
    dosage: str
    instructions: str
    pharmacy_id: int

    class Config:
        from_attributes = True



# PHARMACY SCHEMAS

class PharmacyCreate(BaseModel):
    name: str
    address: str
    contact: str


class PharmacyResponse(BaseModel):
    id: int
    name: str
    address: str
    contact: str

    class Config:
        from_attributes = True


# EMERGENCY SCHEMAS

class EmergencyCreate(BaseModel):
    user_id: int
    message: str


class EmergencyResponse(BaseModel):
    id: int
    user_id: int
    message: str
    timestamp: Optional[datetime] = None
    status: str

    class Config:
        from_attributes = True
