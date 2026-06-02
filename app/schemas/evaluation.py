from pydantic import BaseModel
from datetime import datetime

class EvaluationRequest(BaseModel):
    question: str
    user_answer: str

class EvaluationResponse(BaseModel):
    question_id: int
    score: float
    covered_concepts: list
    missing_concepts: list
    suggestions: str
    improved_answer: str
    
class QuestionResponse(BaseModel):
    id: int
    text: str
    domain: str

class HistoryResponse(BaseModel):
    id: int
    user_answer: str
    score: float
    covered_concepts: list
    missing_concepts: list
    created_at: datetime

class MCQRequest(BaseModel):
    question_id: int
    selected_option: str

class MCQResponse(BaseModel):
    correct: bool
    selected_option: str
    correct_answer: str
    explanation: str