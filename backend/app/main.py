import os
from pathlib import Path
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.config import ALLOWED_ORIGINS
from app.core.database import Base, engine, SessionLocal

from app.models.user import User  # noqa: F401
from app.models.course import Course  # noqa: F401
from app.models.lesson import Lesson  # noqa: F401
from app.models.quiz import Quiz, Question  # noqa: F401
from app.models.attempt import QuizAttempt, QuizAnswer  # noqa: F401

from app.routers import (
    auth, users, courses, lessons, quizzes,
    recommendations, learning, attempts, feedback, ai,
)


def _auto_seed():
    """Seed courses/lessons/quizzes if the database is empty."""
    db = SessionLocal()
    try:
        if db.query(Course).count() > 0:
            print("Database already seeded — skipping.")
            return
        print("Database is empty — running auto-seed...")
        from app.seed import run_seed
        run_seed(db)
        print("Auto-seed complete.")
    except Exception as e:
        print(f"Auto-seed error: {e}")
    finally:
        db.close()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    Base.metadata.create_all(bind=engine)
    _auto_seed()
    yield
    # Shutdown (nothing needed)


app = FastAPI(
    title="AdaptiveLearn AI",
    description="AI-driven adaptive learning platform",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router,            prefix="/api/auth",            tags=["Authentication"])
app.include_router(users.router,           prefix="/api/users",           tags=["Users"])
app.include_router(courses.router,         prefix="/api/courses",         tags=["Courses"])
app.include_router(lessons.router,         prefix="/api/lessons",         tags=["Lessons"])
app.include_router(quizzes.router,         prefix="/api/quizzes",         tags=["Quizzes"])
app.include_router(recommendations.router, prefix="/api/recommendations", tags=["Recommendations"])
app.include_router(learning.router,        prefix="/api/learning",        tags=["Learning"])
app.include_router(attempts.router,        prefix="/api/attempts",        tags=["Attempts"])
app.include_router(ai.router,              prefix="/api/ai",              tags=["AI"])
app.include_router(feedback.router,        prefix="/api/feedback",        tags=["AI Feedback"])


@app.get("/health")
def health():
    return {"status": "healthy"}


# ── Frontend Static Files (Single-service Fullstack Deployment) ─────────────
_static_dir = None
_candidates = [
    Path(os.getenv("FRONTEND_DIST_DIR", "")),
    Path(__file__).resolve().parent.parent.parent / "frontend" / "dist",
    Path(__file__).resolve().parent.parent / "dist",
    Path("/app/frontend/dist"),
    Path("./frontend/dist"),
    Path("./dist"),
]

for _p in _candidates:
    if str(_p) and _p.is_dir() and (_p / "index.html").is_file():
        _static_dir = _p
        break

if _static_dir:
    _assets_dir = _static_dir / "assets"
    if _assets_dir.is_dir():
        app.mount("/assets", StaticFiles(directory=str(_assets_dir)), name="assets")

    @app.get("/{full_path:path}")
    async def serve_spa(full_path: str):
        # Serve exact file if it exists (e.g. favicon.ico, vite.svg)
        candidate = _static_dir / full_path
        if full_path and candidate.is_file():
            return FileResponse(str(candidate))
        # Fallback to index.html for client-side routing (e.g. /dashboard, /courses)
        return FileResponse(str(_static_dir / "index.html"))
else:
    @app.get("/")
    def root():
        return {"message": "AdaptiveLearn AI API is running"}