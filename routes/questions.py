from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Question
from ..database import SessionLocal
from ..models import Question
from sqlalchemy import func


router = APIRouter()



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



@router.get("/questions/{subject}")
def get_questions(subject: str, db: Session = Depends(get_db)):

    questions = db.query(Question).filter(func.lower(Question.subject) == subject.lower()).all()

    if not questions:
        raise HTTPException(status_code=404, detail="No questions found for this subject")
    return [q.to_dict() for q in questions]


@router.get("/debug/questions")
def debug_questions(db: Session = Depends(get_db)):
    return db.query(Question).all()

