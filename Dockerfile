# ── Stage 1: Build Frontend ──────────────────────────────────────────────────
FROM node:20-alpine AS frontend-builder
WORKDIR /frontend
COPY frontend/package*.json ./
RUN npm ci --silent
COPY frontend/ ./
RUN npm run build

# ── Stage 2: Build Backend & Serve Full-stack App ────────────────────────────
FROM python:3.11-slim AS runner
WORKDIR /app

# Install minimal system tools
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy backend application code
COPY backend/app/ ./backend/app/
COPY backend/seed*.py ./backend/

# Copy compiled React frontend
COPY --from=frontend-builder /frontend/dist ./frontend/dist

# Environment variables
ENV PYTHONPATH="/app/backend" \
    PORT=8000 \
    DATABASE_URL="sqlite:///./adaptive_learning.db" \
    ALLOWED_ORIGINS="*" \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

EXPOSE 8000

# Start server on dynamic cloud $PORT
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
