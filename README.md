# AdaptiveLearn AI

An AI-driven adaptive learning platform built with **FastAPI**, **React**, and a **distilgpt2** feedback engine. The platform adjusts quiz difficulty based on learner performance and delivers personalised AI-generated feedback.

---

## Architecture

```
┌─────────────────────────────────────────────────────┐
│                   Browser                           │
│           React SPA  (port 80)                      │
└──────────────────────┬──────────────────────────────┘
                       │  /api/*  proxied by nginx
┌──────────────────────▼──────────────────────────────┐
│              nginx  (frontend container)            │
└──────────────────────┬──────────────────────────────┘
                       │  http://backend:8000
┌──────────────────────▼──────────────────────────────┐
│          FastAPI  (backend container, port 8000)    │
│    Auth · Courses · Quizzes · Adaptive Engine       │
│    LLM Feedback (distilgpt2)                        │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│          SQLite  (Docker volume: db_data)           │
└─────────────────────────────────────────────────────┘
```

| Layer     | Technology                              |
|-----------|-----------------------------------------|
| Frontend  | React 18, Vite 5, React Router v6, Axios |
| Backend   | FastAPI 0.115, Uvicorn, SQLAlchemy 2     |
| Database  | SQLite (volume-persisted)               |
| Auth      | JWT (python-jose) + bcrypt              |
| AI        | Hugging Face Transformers — distilgpt2  |
| Serve     | nginx 1.27 (SPA + reverse proxy)        |

---

## Quick Start — Docker Compose (recommended)

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) ≥ 24
- [Docker Compose](https://docs.docker.com/compose/) ≥ 2.20

### 1. Clone and configure

```bash
git clone <your-repo-url>
cd Adaptive-learning-platform

# Create your .env from the template
cp .env.example .env
```

Open `.env` and set a strong `SECRET_KEY`:

```bash
# Generate one with Python
python -c "import secrets; print(secrets.token_hex(32))"
```

### 2. Build and start

```bash
docker compose up --build
```

> First build downloads the distilgpt2 model weights (~350 MB) and installs all Python/Node dependencies — allow 5–10 minutes.

### 3. Seed sample data (first run only)

While the containers are running, open a second terminal:

```bash
# Create a course + lesson + quiz, then seed questions
docker compose exec backend python -c "
from app.core.database import SessionLocal
from app.models.course import Course
from app.models.lesson import Lesson
from app.models.quiz import Quiz
db = SessionLocal()
c = Course(title='Intro to AI', description='AI fundamentals', difficulty='beginner', category='AI')
db.add(c); db.commit(); db.refresh(c)
l = Lesson(course_id=c.id, title='What is Machine Learning?', content='ML is a subset of AI...', difficulty='beginner', order=1)
db.add(l); db.commit(); db.refresh(l)
q = Quiz(lesson_id=l.id, title='ML Basics Quiz')
db.add(q); db.commit()
db.close()
print('Done — course, lesson, and quiz created')
"

docker compose exec backend python seed_questions.py
```

### 4. Open the app

| URL                              | What you get              |
|----------------------------------|---------------------------|
| http://localhost                 | React frontend            |
| http://localhost:8000/docs       | FastAPI Swagger UI        |
| http://localhost:8000/redoc      | FastAPI ReDoc             |

Register a new account, browse courses, take a quiz, and view AI feedback on the Recommendations page.

---

## Local Development (without Docker)

### Backend

```bash
cd backend

# Create and activate a virtual environment
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate

pip install -r requirements.txt

# Set environment variables (or create a .env file in backend/)
cp ../.env.example .env
# Edit .env: set DATABASE_URL=sqlite:///./adaptive_learning.db

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API available at http://localhost:8000  
Interactive docs at http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

App available at http://localhost:5173  
Vite proxies `/api/*` to `http://localhost:8000` automatically.

---

## Project Structure

```
Adaptive-learning-platform/
├── backend/
│   ├── app/
│   │   ├── core/           # config, database, security, dependencies
│   │   ├── models/         # SQLAlchemy ORM models
│   │   ├── routers/        # FastAPI route handlers
│   │   ├── schemas/        # Pydantic request/response schemas
│   │   ├── services/       # adaptive engine, LLM feedback
│   │   └── main.py         # FastAPI app entry point
│   ├── seed_questions.py   # Sample quiz questions seeder
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── components/     # Reusable UI components
│   │   ├── context/        # React context (auth)
│   │   ├── pages/          # Page-level components
│   │   └── services/       # Axios API client
│   ├── nginx.conf          # Production nginx config
│   ├── vite.config.js
│   └── Dockerfile
├── data/                   # CSV datasets (for notebooks)
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## API Reference (key endpoints)

| Method | Path | Description |
|--------|------|-------------|
| POST | `/api/auth/register` | Create a new account |
| POST | `/api/auth/login` | Login → returns JWT |
| GET | `/api/users/me` | Current user profile (auth required) |
| GET | `/api/courses/` | List all courses |
| GET | `/api/courses/{id}` | Course detail + lessons |
| GET | `/api/quizzes/{id}` | Quiz + questions |
| POST | `/api/attempts/start` | Start a quiz attempt |
| POST | `/api/attempts/{id}/answer` | Submit a single answer |
| GET | `/api/recommendations/` | Performance analysis |
| GET | `/api/feedback/` | AI-generated tutor feedback |
| GET | `/health` | Health check |

Full interactive docs at `/docs` (Swagger UI).

---

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `change-me-in-production` | JWT signing key — **must be changed** |
| `ALGORITHM` | `HS256` | JWT algorithm |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `60` | Token lifetime |
| `DATABASE_URL` | SQLite path | SQLAlchemy DB connection string |
| `ALLOWED_ORIGINS` | `http://localhost` | Comma-separated CORS allowed origins |

---

## Production Checklist

- [ ] Set a strong random `SECRET_KEY` in `.env`
- [ ] Set `ALLOWED_ORIGINS` to your actual domain
- [ ] Add HTTPS via a reverse proxy (Caddy, nginx with Let's Encrypt, etc.)
- [ ] Switch to PostgreSQL for multi-instance deployments
- [ ] Set up automated database backups for the `db_data` volume
- [ ] Pin Docker image digests for reproducible builds

---

## License

MIT
