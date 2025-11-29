from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import *
from datetime import datetime, timedelta
import random

Base.metadata.create_all(bind=engine)
db: Session = SessionLocal()

try:
    # ---------------- USERS (patients + admin) ----------------
    users = [
        User(name="Alice Johnson", email="alice@email.com", password="pass123", role="patient", phone="555-1231", address="123 Maple St"),
        User(name="Brian Lee", email="brian@email.com", password="pass123", role="patient", phone="555-1232", address="47 Oak Ave"),
        User(name="Catherine Diaz", email="catherine@email.com", password="pass123", role="patient", phone="555-1233", address="9 Birch Blvd"),
        User(name="Daniel Kim", email="daniel@email.com", password="pass123", role="patient", phone="555-1234", address="56 Elm Rd"),
        User(name="Emma Wilson", email="emma@email.com", password="pass123", role="patient", phone="555-1235", address="89 Cedar Ct"),
        User(name="System Admin", email="admin@email.com", password="admin123", role="admin", phone="555-0000", address="Head Office"),
    ]
    db.add_all(users)

    # ---------------- DOCTORS ----------------
    doctors = [
        Doctor(name="Dr. Emily Carter", email="emily@clinic.com", password="doctor123", role="doctor", contact_number="555-2001", license_no="LIC-001"),
        Doctor(name="Dr. James Miller", email="james@wellness.com", password="doctor123", role="doctor", contact_number="555-2002", license_no="LIC-002"),
        Doctor(name="Dr. Sophia Zhang", email="sophia@therapy.com", password="doctor123", role="doctor", contact_number="555-2003", license_no="LIC-003"),
    ]
    db.add_all(doctors)

    # ---------------- PHARMACIES ----------------
    pharmacies = [
        Pharmacy(name="MindWell Pharmacy", address="120 Oak Street", contact_number="555-2111"),
        Pharmacy(name="Serenity Meds", address="410 Pine Drive", contact_number="555-3222"),
        Pharmacy(name="WellBeing Center", address="86 Birch Road", contact_number="555-4333"),
    ]
    db.add_all(pharmacies)
    db.commit()

    # ---------------- ASSESSMENTS ----------------
    mood_labels = ["Happy", "Calm", "Anxious", "Depressed", "Neutral"]
    recommendations = [
        "Practice breathing exercises",
        "Take a walk outside",
        "Journal your feelings",
        "Schedule a therapy session",
        "Maintain healthy sleep"
    ]

    assessments = [
        Assessment(
            user_id=random.randint(1, 6),
            doctor_id=random.randint(1, 3),
            mood_score=random.uniform(2.5, 9.5),
            mood_label=random.choice(mood_labels),
            recommendation=random.choice(recommendations),
            created_at=datetime.utcnow() - timedelta(days=random.randint(0, 10))
        )
        for _ in range(20)
    ]
    db.add_all(assessments)
    db.commit()

    # ---------------- CONSULTATIONS ----------------
    consultations = [
        Consultation(
            user_id=random.randint(1, 6),
            doctor_id=random.randint(1, 3),
            date=datetime.utcnow() - timedelta(days=random.randint(1, 7)),
            notes=random.choice([
                "Follow-up scheduled.",
                "Discussed coping mechanisms.",
                "Patient mood improving.",
                "Medication side effects mild."
            ])
        )
        for _ in range(15)
    ]
    db.add_all(consultations)
    db.commit()

    # ---------------- PRESCRIPTIONS ----------------
    meds = [
        ("Sertraline", "50mg", "Once daily after breakfast"),
        ("Fluoxetine", "20mg", "Morning dose"),
        ("Duloxetine", "30mg", "Twice daily"),
        ("Escitalopram", "10mg", "Night dose")
    ]
    prescriptions = [
        Prescription(
            consultation_id=random.randint(1, 15),
            doctor_id=random.randint(1, 3),
            pharmacy_id=random.randint(1, 3),
            medication=med,
            dosage=dose,
            instructions=inst
        )
        for med, dose, inst in random.choices(meds, k=15)
    ]
    db.add_all(prescriptions)
    db.commit()

    # ---------------- MOOD HISTORY ----------------
    moods = ["Happy", "Calm", "Sad", "Tired", "Energetic"]
    mood_history = [
        MoodHistory(
            user_id=random.randint(1, 6),
            mood_label=random.choice(moods),
            mood_score=random.uniform(2.0, 9.0),
            timestamp=datetime.utcnow() - timedelta(hours=random.randint(1, 120))
        )
        for _ in range(30)
    ]
    db.add_all(mood_history)
    db.commit()

    # ---------------- EMERGENCIES ----------------
    emergencies = [
        Emergency(user_id=random.randint(1, 6), notes="Severe panic attack", resolved=False),
        Emergency(user_id=random.randint(1, 6), notes="Feeling hopeless and anxious", resolved=True),
        Emergency(user_id=random.randint(1, 6), notes="Unable to sleep for 3 days", resolved=False)
    ]
    db.add_all(emergencies)
    db.commit()

    # ---------------- RECOMMENDATIONS ----------------
    activity_list = [
        ("Meditation", "10-minute mindfulness meditation each morning"),
        ("Light Exercise", "Short 15-minute walk daily"),
        ("Gratitude Journal", "Write down 3 positive moments per day"),
        ("Social Connection", "Call a friend or family member"),
        ("Balanced Diet", "Include more fruits and vegetables")
    ]
    recs = [
        Recommendation(
            assessment_id=random.randint(1, 20),
            activity_name=act,
            description=desc
        )
        for act, desc in random.choices(activity_list, k=10)
    ]
    db.add_all(recs)
    db.commit()

    print("Data inserted successfully!")

except Exception as e:
    db.rollback()
    print("Error inserting data:", e)

finally:
    db.close()
