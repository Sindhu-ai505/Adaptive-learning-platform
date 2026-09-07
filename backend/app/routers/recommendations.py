from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.adaptive_engine import (
    analyze_performance,
    calculate_next_difficulty,
    get_adaptive_questions
)
router = APIRouter()


@router.get("/")
def get_recommendation(
    user_id: int,
    quiz_id: int,
    db: Session = Depends(get_db)
):
    return analyze_performance(
        user_id=user_id,
        quiz_id=quiz_id,
        db=db
    )
@router.get("/difficulty")
def get_next_difficulty(score: float):
    difficulty = calculate_next_difficulty(score)

    return {
        "score": score,
        "next_difficulty": difficulty
    }
@router.get("/questions")
def get_adaptive_questions_endpoint(
    quiz_id: int,
    difficulty: str,
    db: Session = Depends(get_db)
):
    questions = get_adaptive_questions(
        db=db,
        quiz_id=quiz_id,
        difficulty=difficulty,
        limit=5
    )

    return {
        "quiz_id": quiz_id,
        "difficulty": difficulty,
        "count": len(questions),
        "questions": [
            {
                "id": question.id,
                "question": question.question_text,
                "option_a": question.option_a,
                "option_b": question.option_b,
                "option_c": question.option_c,
                "option_d": question.option_d
            }
            for question in questions
        ]
    }