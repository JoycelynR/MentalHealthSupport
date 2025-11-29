from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import Assessment, MoodHistory
from schemas import AssessmentCreate
from crud import assessment_crud  # if you have one

router = APIRouter(prefix="/assessments", tags=["Assessments"]) 

@router.post("")
@router.post("/")
def create_assessment(assessment: AssessmentCreate, db: Session = Depends(get_db)):
    new_assessment = assessment_crud.create_assessment(db, assessment)
    response = {
        "id": new_assessment.id,
        "user_id": new_assessment.user_id,
        "mood_score": new_assessment.mood_score,
        "recommendation": new_assessment.recommendation,
        "created_at": new_assessment.created_at,
    }
    print("Returning assessment:", response)  
    return response

@router.get("")
@router.get("/")
def get_all_assessments(db: Session = Depends(get_db)):
    return assessment_crud.get_all_assessments(db)
@router.get("/user/{user_id}")
def get_assessments_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(Assessment).filter(Assessment.user_id == user_id).all()

@router.get("/patient/{user_id}")
def get_assessments_for_patient(user_id: int, db: Session = Depends(get_db)):
    assessments = (
        db.query(Assessment)
        .filter(Assessment.user_id == user_id)
        .order_by(Assessment.created_at.desc())
        .all()
    )

    if not assessments:
        return []

    result = []
    for a in assessments:
        result.append({
            "id": a.id,
            "date": a.created_at,
            "mood_score": a.mood_score,
            "mood_label": a.mood_label,
            "recommendation": a.recommendation
        })

    return result