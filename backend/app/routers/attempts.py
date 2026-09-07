from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.quiz import Quiz, Question
from app.models.attempt import QuizAttempt, QuizAnswer


router = APIRouter()


@router.post("/start")
def start_attempt(
    user_id: int,
    quiz_id: int,
    db: Session = Depends(get_db)
):
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    questions = db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).all()

    if not questions:
        raise HTTPException(
            status_code=400,
            detail="Quiz has no questions"
        )

    attempt = QuizAttempt(
        user_id=user_id,
        quiz_id=quiz_id,
        total_questions=len(questions),
        correct_answers=0,
        score=0
    )

    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return attempt


@router.post("/{attempt_id}/answer")
def submit_answer(
    attempt_id: int,
    question_id: int,
    selected_answer: str,
    db: Session = Depends(get_db)
):
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Attempt not found"
        )

    question = db.query(Question).filter(
        Question.id == question_id
    ).first()

    if not question:
        raise HTTPException(
            status_code=404,
            detail="Question not found"
        )

    selected_answer = selected_answer.upper()

    if selected_answer not in ["A", "B", "C", "D"]:
        raise HTTPException(
            status_code=400,
            detail="Answer must be A, B, C or D"
        )

    is_correct = (
        selected_answer == question.correct_answer
    )

    answer = QuizAnswer(
        attempt_id=attempt_id,
        question_id=question_id,
        selected_answer=selected_answer,
        is_correct=is_correct
    )

    db.add(answer)

    if is_correct:
        attempt.correct_answers += 1

    if attempt.total_questions > 0:
        attempt.score = (
            attempt.correct_answers
            / attempt.total_questions
        ) * 100

    db.commit()
    db.refresh(attempt)

    return {
        "question_id": question_id,
        "selected_answer": selected_answer,
        "is_correct": is_correct,
        "current_score": attempt.score
    }


@router.get("/{attempt_id}")
def get_attempt(
    attempt_id: int,
    db: Session = Depends(get_db)
):
    attempt = db.query(QuizAttempt).filter(
        QuizAttempt.id == attempt_id
    ).first()

    if not attempt:
        raise HTTPException(
            status_code=404,
            detail="Attempt not found"
        )

    answers = db.query(QuizAnswer).filter(
        QuizAnswer.attempt_id == attempt_id
    ).all()

    return {
        "attempt": attempt,
        "answers": answers
    }