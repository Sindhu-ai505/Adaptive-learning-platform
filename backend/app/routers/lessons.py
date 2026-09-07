from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.course import Course
from app.models.lesson import Lesson


router = APIRouter()


@router.post("/")
def create_lesson(
    course_id: int,
    title: str,
    content: str = "",
    difficulty: str = "beginner",
    order: int = 1,
    db: Session = Depends(get_db)
):
    course = db.query(Course).filter(
        Course.id == course_id
    ).first()

    if not course:
        raise HTTPException(
            status_code=404,
            detail="Course not found"
        )

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


@router.get("/")
def get_lessons(
    course_id: int | None = None,
    db: Session = Depends(get_db)
):
    query = db.query(Lesson)

    if course_id is not None:
        query = query.filter(
            Lesson.course_id == course_id
        )

    return query.order_by(Lesson.order).all()


@router.get("/{lesson_id}")
def get_lesson(
    lesson_id: int,
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

    return lesson