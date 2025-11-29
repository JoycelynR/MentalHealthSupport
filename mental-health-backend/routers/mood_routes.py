from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import MoodHistory

router = APIRouter(prefix="/mood_history", tags=["Mood History"])

@router.get("/")
def get_all_mood_history(db: Session = Depends(get_db)):
    return db.query(MoodHistory).all()

@router.get("/user/{user_id}")
@router.get("/user/{user_id}/") 
def get_mood_history_by_user(user_id: int, db: Session = Depends(get_db)):
    return db.query(MoodHistory).filter(MoodHistory.user_id == user_id).all()
