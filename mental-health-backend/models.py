from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, Boolean
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# USER TABLE

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False)  # patient, doctor, admin
    phone = Column(String(20))
    address = Column(String(255))

    # Relationships
    assessments = relationship("Assessment", back_populates="user")
    consultations = relationship("Consultation", back_populates="user")
    emergencies = relationship("Emergency", back_populates="user")
    mood_history = relationship("MoodHistory", back_populates="user")



# DOCTOR TABLE

class Doctor(Base):
    __tablename__ = "doctors"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(255))
    role = Column(String(20))
    contact_number = Column(String(20))
    license_no = Column(String(50))

    consultations = relationship("Consultation", back_populates="doctor")
    prescriptions = relationship("Prescription", back_populates="doctor")
    assessments = relationship("Assessment", back_populates="doctor")

# ASSESSMENT TABLE

class Assessment(Base):
    __tablename__ = "assessments"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=True)
    mood_score = Column(Float)
    mood_label = Column(String(50))  # e.g., Happy, Sad, Neutral
    recommendation = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="assessments")
    doctor = relationship("Doctor", back_populates="assessments")
    recommendations = relationship("Recommendation", back_populates="assessment")



# CONSULTATION TABLE

class Consultation(Base):
    __tablename__ = "consultations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    date = Column(DateTime, default=datetime.utcnow)
    notes = Column(Text)

    user = relationship("User", back_populates="consultations")
    doctor = relationship("Doctor", back_populates="consultations")
    prescriptions = relationship("Prescription", back_populates="consultation")



# PRESCRIPTION TABLE

class Prescription(Base):
    __tablename__ = "prescriptions"
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    doctor_id = Column(Integer, ForeignKey("doctors.id"))
    pharmacy_id = Column(Integer, ForeignKey("pharmacies.id"), nullable=True)
    medication = Column(Text)
    dosage = Column(String(100))
    instructions = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    consultation = relationship("Consultation", back_populates="prescriptions")
    doctor = relationship("Doctor", back_populates="prescriptions")
    pharmacy = relationship("Pharmacy", back_populates="prescriptions")



# PHARMACY TABLE

class Pharmacy(Base):
    __tablename__ = "pharmacies"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    address = Column(String(255))
    contact_number = Column(String(20))

    prescriptions = relationship("Prescription", back_populates="pharmacy")



# EMERGENCY TABLE

class Emergency(Base):
    __tablename__ = "emergencies"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    resolved = Column(Boolean, default=False)
    notes = Column(Text)

    user = relationship("User", back_populates="emergencies")



# RECOMMENDED ACTIVITIES TABLE

class Recommendation(Base):
    __tablename__ = "recommendations"
    id = Column(Integer, primary_key=True, index=True)
    assessment_id = Column(Integer, ForeignKey("assessments.id"))
    activity_name = Column(String(100))
    description = Column(Text)

    assessment = relationship("Assessment", back_populates="recommendations")


# MOOD HISTORY TABLE

class MoodHistory(Base):
    __tablename__ = "mood_history"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    mood_label = Column(String(50))
    mood_score = Column(Float)
    timestamp = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="mood_history")
