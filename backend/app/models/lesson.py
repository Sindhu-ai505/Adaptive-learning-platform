from sqlalchemy import Column, Integer, String, Text, ForeignKey

from app.core.database import Base


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    course_id = Column(
        Integer,
        ForeignKey("courses.id"),
        nullable=False
    )

    title = Column(
        String(200),
        nullable=False
    )

    content = Column(
        Text,
        nullable=True
    )

    difficulty = Column(
        String(50),
        default="beginner"
    )

    order = Column(
        Integer,
        default=1
    )