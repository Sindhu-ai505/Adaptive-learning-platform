from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.lesson import Lesson
from app.models.quiz import Quiz, Question


router = APIRouter()


@router.post("/")
def create_quiz(
    lesson_id: int,
    title: str,
    db: Session = Depends(get_db)
):
    lesson = db.query(Lesson).filter(
        Lesson.id == lesson_id
    ).first()

    if not lesson:
        raise HTTPException(
            status_code=404,
            detail="Lesson not found"
        )

    quiz = Quiz(
        lesson_id=lesson_id,
        title=title
    )

    db.add(quiz)
    db.commit()
    db.refresh(quiz)

    return quiz


@router.post("/{quiz_id}/questions")
def create_question(
    quiz_id: int,
    question_text: str,
    option_a: str,
    option_b: str,
    option_c: str,
    option_d: str,
    correct_answer: str,
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

    if correct_answer.upper() not in ["A", "B", "C", "D"]:
        raise HTTPException(
            status_code=400,
            detail="correct_answer must be A, B, C or D"
        )

    question = Question(
        quiz_id=quiz_id,
        question_text=question_text,
        option_a=option_a,
        option_b=option_b,
        option_c=option_c,
        option_d=option_d,
        correct_answer=correct_answer.upper()
    )

    db.add(question)
    db.commit()
    db.refresh(question)

    return question


@router.get("/by-lesson/{lesson_id}")
def get_quiz_by_lesson(
    lesson_id: int,
    db: Session = Depends(get_db)
):
    """Return the quiz (and its questions) for a given lesson_id."""
    quiz = db.query(Quiz).filter(Quiz.lesson_id == lesson_id).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail=f"No quiz found for lesson {lesson_id}"
        )

    questions = db.query(Question).filter(
        Question.quiz_id == quiz.id
    ).all()

    return {
        "quiz": quiz,
        "questions": questions
    }


@router.get("/{quiz_id}")
def get_quiz(
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

    return {
        "quiz": quiz,
        "questions": questions
    }
@router.post("/{quiz_id}/submit")
def submit_quiz(
    quiz_id: int,
    answers: dict,
    db: Session = Depends(get_db)
):
    # Check whether quiz exists
    quiz = db.query(Quiz).filter(
        Quiz.id == quiz_id
    ).first()

    if not quiz:
        raise HTTPException(
            status_code=404,
            detail="Quiz not found"
        )

    # Get all questions belonging to this quiz
    questions = db.query(Question).filter(
        Question.quiz_id == quiz_id
    ).all()

    if not questions:
        raise HTTPException(
            status_code=404,
            detail="No questions found for this quiz"
        )

    correct = 0
    total = len(questions)

    # Check answers
    for question in questions:

        # Answers are sent like {"1": "A", "2": "C"}
        selected_answer = answers.get(str(question.id))

        if selected_answer:
            if selected_answer.upper() == question.correct_answer.upper():
                correct += 1

    # Calculate percentage
    percentage = (correct / total) * 100

    # Adaptive difficulty
    if percentage >= 80:
        next_difficulty = "hard"
    elif percentage >= 50:
        next_difficulty = "medium"
    else:
        next_difficulty = "easy"

    return {
        "quiz_id": quiz_id,
        "score": correct,
        "total": total,
        "percentage": round(percentage, 2),
        "next_difficulty": next_difficulty
    }