from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Question, Evaluation, ReferenceAnswer
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

@router.get("/questions/options/{question_id}")
def get_options(question_id: int, db: Session = Depends(get_db)):
    reference = db.query(ReferenceAnswer)\
        .filter(ReferenceAnswer.question_id == question_id)\
        .first()
    if not reference or not reference.options:
        return {"options": []}
    return {"options": reference.options}