from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.adaptive_engine import analyze_performance
from app.services.llm_service import generate_feedback


router = APIRouter()


@router.get("/")
def get_ai_feedback(
    user_id: int,
    quiz_id: int,
    db: Session = Depends(get_db)
):
    performance = analyze_performance(
        user_id=user_id,
        quiz_id=quiz_id,
        db=db
    )

    if "message" in performance:
        raise HTTPException(
            status_code=404,
            detail=performance["message"]
        )

    feedback = generate_feedback(
        score=performance["score"],
        level=performance["level"],
        recommendation=performance["recommendation"]
    )

    return {
        "performance": performance,
        "ai_feedback": feedback
    }