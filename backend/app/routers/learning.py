from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.lesson import Lesson


router = APIRouter()


@router.post("/lessons")
def create_lesson(
    course_id: int,
    title: str,
    content: str = "",
    difficulty: str = "beginner",
    order: int = 1,
    db: Session = Depends(get_db)
):

    lesson = Lesson(
        course_id=course_id,
        title=title,
        content=content,
        difficulty=difficulty,
        order=order
    )

    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    return lesson


@router.get("/lessons/{course_id}")
def get_lessons(
    course_id: int,
    db: Session = Depends(get_db)
):

    return db.query(Lesson).filter(
        Lesson.course_id == course_id
    ).order_by(Lesson.order).all()