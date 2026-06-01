from app.db.session import Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey, JSON, DateTime, func
from pgvector.sqlalchemy import Vector

class Question(Base):
    __tablename__ = "questions"

    id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    domain = Column(String, nullable=False)
    difficulty = Column(String, nullable=False, server_default="easy")

class ReferenceAnswer(Base):
    __tablename__ = "reference_answers"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    answer = Column(String, nullable=False)
    key_concepts = Column(JSON, nullable=False)
    embedding = Column(Vector(384), nullable=False)

class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    user_answer = Column(String, nullable=False)
    score = Column(Float, nullable=False)
    covered_concepts = Column(JSON, nullable=False)
    missing_concepts = Column(JSON, nullable=False)
    suggestions = Column(String, nullable=False)
    improved_answer = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)