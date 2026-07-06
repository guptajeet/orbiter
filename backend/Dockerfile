# Build stage
FROM python:3.11-slim AS builder
WORKDIR /app
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# Production stage
FROM python:3.11-slim AS production
WORKDIR /app

# Create non-root user
RUN groupadd -r orbiter && useradd -r -g orbiter -d /app -s /sbin/nologin orbiter

# Copy installed packages from builder
COPY --from=builder /install /usr/local

# Copy application code
COPY backend/ /app/backend/
COPY config/ /app/config/
COPY prompts/ /app/prompts/

# Create data directory
RUN mkdir -p /app/data && chown -R orbiter:orbiter /app

# Switch to non-root user
USER orbiter

ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/api/health')" || exit 1

EXPOSE 8000

CMD ["python", "-m", "uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
