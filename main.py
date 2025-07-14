from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from datetime import datetime
from typing import List
from schemas import QuestionSchema
from models import Question

from database import Base, engine, get_db
from models import Student, Score
from schemas import StudentSchema, ScoreSubmission

import json
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.post("/register")
def register(student: StudentSchema, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(Student.username == student.username).first()
    if db_student:
        raise HTTPException(status_code=400, detail="Username already exists")
    new_student = Student(**student.dict())
    db.add(new_student)
    db.commit()
    return {"message": "Registration successful"}

@app.post("/login")
def login(student: StudentSchema, db: Session = Depends(get_db)):
    db_student = db.query(Student).filter(
        Student.username == student.username,
        Student.password == student.password
    ).first()
    if not db_student:
        raise HTTPException(status_code=400, detail="Invalid username or password")
    return {"message": "Login successful", "fullname": db_student.fullname}

import random

@app.get("/questions/{subject}", response_model=List[QuestionSchema])
def get_questions(subject: str, db: Session = Depends(get_db)):
    db_questions = db.query(Question).filter(Question.subject == subject).all()
    random.shuffle(db_questions)  # Shuffle the list
    selected_questions = db_questions[:20]  # Limit to 20

    result = []
    for q in selected_questions:
        result.append({
            "id": q.id,
            "subject": q.subject,
            "question": q.question,
            "options": {
                "A": q.option_a,
                "B": q.option_b,
                "C": q.option_c,
                "D": q.option_d
            },
            "answer": q.correct_option
        })

    return result

@app.get("/leaderboard/{subject}")
def get_leaderboard(subject: str, db: Session = Depends(get_db)):
    top_scores = db.query(Score).filter(Score.subject == subject).order_by(Score.score.desc()).limit(10).all()
    return {
        "leaderboard": [
            {
                "username": s.username,
                "score": s.score,
                "entered_on": s.timestamp,
                "time_taken": s.time_taken
            } for s in top_scores
        ]
    }
