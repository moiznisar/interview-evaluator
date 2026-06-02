from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.db.models import Question, ReferenceAnswer, Evaluation
from app.schemas.evaluation import EvaluationRequest, EvaluationResponse, MCQRequest, MCQResponse
from app.core.embeddings import get_embedding
from app.core.similarity import compute_similarity
from app.core.rag import generate_feedback

router = APIRouter()

@router.post("/evaluate", response_model=EvaluationResponse)
def evaluate(request: EvaluationRequest, db: Session = Depends(get_db)):

    user_embedding = get_embedding(request.user_answer)

    reference = db.query(ReferenceAnswer)\
        .order_by(ReferenceAnswer.embedding.cosine_distance(user_embedding))\
        .first()

    similarity_score = compute_similarity(reference.embedding, user_embedding)

    covered = [c for c in reference.key_concepts if c.lower() in request.user_answer.lower()]
    missing = [c for c in reference.key_concepts if c.lower() not in request.user_answer.lower()]

    concept_score = (len(covered) / len(reference.key_concepts)) * 100 if reference.key_concepts else 0
    score = round((similarity_score * 0.5) + (concept_score * 0.5), 2)

    question = db.query(Question).filter(Question.id == reference.question_id).first()

    if not missing:
        suggestions = "Great answer! You covered all the key concepts."
        improved_answer = "Your answer is already strong. Keep it concise and confident in the actual interview."
    else:
        bullet_points = "\n".join([f"• {concept}" for concept in missing])
        suggestions = f"Your answer was missing these key points:\n{bullet_points}"

        feedback = generate_feedback(
            question=question.text,
            user_answer=request.user_answer,
            reference_answer=reference.answer,
            missing_concepts=missing,
            score=similarity_score
        )

        improved_answer = ""
        if "IMPROVED ANSWER:" in feedback:
            parts = feedback.split("IMPROVED ANSWER:")
            improved_answer = parts[1].strip()
        else:
            improved_answer = feedback

    evaluation = Evaluation(
        question_id=reference.question_id,
        user_answer=request.user_answer,
        score=score,
        covered_concepts=covered,
        missing_concepts=missing,
        suggestions=suggestions,
        improved_answer=improved_answer
    )
    db.add(evaluation)
    db.commit()
    db.refresh(evaluation)

    return EvaluationResponse(
        question_id=reference.question_id,
        score=score,
        covered_concepts=covered,
        missing_concepts=missing,
        suggestions=suggestions,
        improved_answer=improved_answer
    )

@router.post("/evaluate/mcq", response_model=MCQResponse)
def evaluate_mcq(request: MCQRequest, db: Session = Depends(get_db)):

    # Get reference answer for this question
    reference = db.query(ReferenceAnswer)\
        .filter(ReferenceAnswer.question_id == request.question_id)\
        .first()

    if not reference or not reference.options:
        return MCQResponse(
            correct=False,
            selected_option=request.selected_option,
            correct_answer="No options available for this question",
            explanation="This question does not have MCQ options."
        )

    correct_answer = reference.options[0]
    is_correct = request.selected_option == correct_answer

    if is_correct:
        explanation = f"Correct! {correct_answer}"
    else:
        explanation = f"Not quite. The correct answer is: {correct_answer}"

    return MCQResponse(
        correct=is_correct,
        selected_option=request.selected_option,
        correct_answer=correct_answer,
        explanation=explanation
    )