from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.course import Course
from app.models.lesson import Lesson

router = APIRouter()


@router.post("/")
def create_course(
    title: str,
    description: str = "",
    difficulty: str = "beginner",
    category: str = "",
    db: Session = Depends(get_db)
):
    course = Course(
        title=title,
        description=description,
        difficulty=difficulty,
        category=category
    )

    db.add(course)
    db.commit()
    db.refresh(course)

    return course


@router.get("/")
def get_courses(
    db: Session = Depends(get_db)
):
    return db.query(Course).all()


@router.get("/{course_id}")
def get_course(
    course_id: int,
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

    lessons = db.query(Lesson).filter(
        Lesson.course_id == course_id
    ).order_by(Lesson.order).all()

    return {
        "course": course,
        "lessons": lessons
    }