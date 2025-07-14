from pydantic import BaseModel
from typing import Optional, Dict

class StudentSchema(BaseModel):
    username: str
    password: str
    fullname: Optional[str] = None

class QuestionSchema(BaseModel):
    id: int
    subject: str
    question: str
    options: Dict[str, str]  # A dictionary of option letters to their texts
    answer: str

class ScoreSubmission(BaseModel):
    username: str
    subject: str
    score: int
    time_taken: int = 1200  # 20 minutes
