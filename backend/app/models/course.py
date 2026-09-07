from sqlalchemy import Column, Integer, String, Text

from app.core.database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    title = Column(
        String(200),
        nullable=False
    )

    description = Column(
        Text,
        nullable=True
    )

    difficulty = Column(
        String(50),
        default="beginner"
    )

    category = Column(
        String(100),
        nullable=True
    )