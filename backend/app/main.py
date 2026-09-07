from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import ALLOWED_ORIGINS
from app.core.database import Base, engine

# Import models so SQLAlchemy registers them before create_all
from app.models.user import User  # noqa: F401
from app.models.course import Course  # noqa: F401
from app.models.lesson import Lesson  # noqa: F401
from app.models.quiz import Quiz, Question  # noqa: F401
from app.models.attempt import QuizAttempt, QuizAnswer  # noqa: F401

from app.routers import (
    auth,
    users,
    courses,
    lessons,
    quizzes,
    recommendations,
    learning,
    attempts,
    feedback,
    ai,
)

# Create all tables on startup
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AdaptiveLearn AI",
    description="AI-driven adaptive learning platform",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(courses.router, prefix="/api/courses", tags=["Courses"])
app.include_router(lessons.router, prefix="/api/lessons", tags=["Lessons"])
app.include_router(quizzes.router, prefix="/api/quizzes", tags=["Quizzes"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(learning.router, prefix="/api/learning", tags=["Learning"])
app.include_router(attempts.router, prefix="/api/attempts", tags=["Attempts"])
app.include_router(ai.router, prefix="/api/ai", tags=["AI"])
app.include_router(feedback.router, prefix="/api/feedback", tags=["AI Feedback"])


@app.get("/")
def root():
    return {"message": "AdaptiveLearn AI API is running"}


@app.get("/health")
def health():
    return {"status": "healthy"}
