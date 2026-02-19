# ────────────────────────────────────────
#  Builder stage
# ────────────────────────────────────────
FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Optional: use uv for faster installs (very popular in 2025–2026)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

COPY requirements.txt .
RUN uv pip install --system --no-cache -r requirements.txt

# ────────────────────────────────────────
#  Final stage
# ────────────────────────────────────────
FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/app/.local/bin:$PATH"

# Create non-root user (security best practice)
RUN useradd --create-home appuser

COPY --from=builder /usr/local/lib/python3.12/site-packages/ /usr/local/lib/python3.12/site-packages/
COPY --from=builder /usr/local/bin/ /usr/local/bin/

# Copy project code
COPY . .

# Fix permissions
RUN chown -R appuser:appuser /app

USER appuser

# Default command (overwritten in docker-compose for dev/prod)
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]