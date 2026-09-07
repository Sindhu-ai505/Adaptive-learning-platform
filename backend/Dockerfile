# ── Stage 1: builder ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build tools needed for some wheels (bcrypt, cryptography, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libffi-dev \
        libssl-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip \
    && pip install --prefix=/install --no-cache-dir -r requirements.txt


# ── Stage 2: runtime ──────────────────────────────────────────────────────────
FROM python:3.11-slim AS runtime

WORKDIR /app

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application source
COPY app/ ./app/

# Persistent volume for the SQLite database
VOLUME ["/app/data"]

# Runtime environment (overridden by docker-compose / k8s secrets)
ENV DATABASE_URL="sqlite:////app/data/adaptive_learning.db" \
    SECRET_KEY="change-me-in-production" \
    ALGORITHM="HS256" \
    ACCESS_TOKEN_EXPIRE_MINUTES="60" \
    ALLOWED_ORIGINS="http://localhost:5173" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

# Run with a single worker; scale horizontally with multiple containers
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
