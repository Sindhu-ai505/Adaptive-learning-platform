from sqlalchemy import Column, Integer, Boolean, Float, ForeignKey, String
from app.core.database import Base


class QuizAttempt(Base):
    __tablename__ = "quiz_attempts"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    quiz_id = Column(
        Integer,
        ForeignKey("quizzes.id"),
        nullable=False
    )

    score = Column(
        Float,
        default=0
    )

    total_questions = Column(
        Integer,
        default=0
    )

    correct_answers = Column(
        Integer,
        default=0
    )


class QuizAnswer(Base):
    __tablename__ = "quiz_answers"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    attempt_id = Column(
        Integer,
        ForeignKey("quiz_attempts.id"),
        nullable=False
    )

    question_id = Column(
        Integer,
        ForeignKey("questions.id"),
        nullable=False
    )

    selected_answer = Column(
        String(1),
        nullable=False
    )

    is_correct = Column(
        Boolean,
        default=False
    )