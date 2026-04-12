from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Question, Evaluation
from app.schemas.evaluation import QuestionResponse, HistoryResponse

router = APIRouter()

@router.get("/questions", response_model=list[QuestionResponse])
def get_questions(db: Session = Depends(get_db)):
    questions = db.query(Question).all()
    return questions

@router.get("/history/{question_id}", response_model=list[HistoryResponse])
def get_history(question_id: int, db: Session = Depends(get_db)):
    history = db.query(Evaluation).filter(Evaluation.question_id == question_id).all()
    return history