from sqlalchemy.orm import Session
from sqlalchemy import func
from models import Assessment, User, Consultation, Doctor, MoodHistory
from schemas import AssessmentCreate
from datetime import datetime


# Simple rule-based recommendations

def generate_recommendation(score: int) -> str:
    if score >= 8:
        return "You seem in great spirits! Keep maintaining your healthy habits and balance."
    elif 5 <= score < 8:
        return "Your mood seems stable. Try a short walk, light exercise, or journaling."
    elif 3 <= score < 5:
        return "You may be feeling low. Consider connecting with a friend or taking a break from screens."
    else:
        return "Your mood indicates stress or sadness. It may help to rest, meditate, or talk to a counselor."
    

# CRUD operations

def create_assessment(db: Session, assessment: AssessmentCreate):
    user = db.query(User).filter(User.id == assessment.user_id).first()
    if not user:
        raise ValueError(f"User with id {assessment.user_id} not found")

    auto_recommendation = generate_recommendation(assessment.mood_score)

    # Create Assessment
    db_assessment = Assessment(
        user_id=assessment.user_id,
        mood_score=assessment.mood_score,
        recommendation=auto_recommendation,
        created_at=datetime.utcnow()
    )
    db.add(db_assessment)

    # Store score in mood history 
    mood_entry = MoodHistory(
        user_id=assessment.user_id,
        mood_score=assessment.mood_score
        # mood_label NOT INCLUDED
    )
    db.add(mood_entry)

    db.commit()
    db.refresh(db_assessment)

    # Auto-consultation for low score
    if assessment.mood_score < 6:
        doctor = db.query(Doctor).order_by(func.random()).first()
        if doctor:
            new_consult = Consultation(
                user_id=assessment.user_id,
                doctor_id=doctor.id,
                notes=f"Auto-generated: Mood score {assessment.mood_score}. Doctor {doctor.name} assigned."
            )
            db.add(new_consult)
            db.commit()
            db.refresh(new_consult)

    return db_assessment


def get_all_assessments(db: Session):
    return db.query(Assessment).all()


def get_assessment_by_user(db: Session, user_id: int):
    return db.query(Assessment).filter(Assessment.user_id == user_id).all()


def delete_assessment(db: Session, assessment_id: int):
    assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
    if not assessment:
        return None
    db.delete(assessment)
    db.commit()
    return assessment
