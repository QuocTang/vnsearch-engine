# Multi-stage Dockerfile for IRS API
# Stage 1: Builder - Install dependencies
FROM python:3.12-slim as builder

# Set working directory
WORKDIR /app

# Install uv for faster package installation
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml .

# Install dependencies using uv
RUN uv pip install --system --no-cache -r pyproject.toml

# Stage 2: Runtime - Minimal production image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Create non-root user
RUN useradd -m -u 1000 irs_user && \
    chown -R irs_user:irs_user /app

# Copy installed packages from builder
COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY --chown=irs_user:irs_user app ./app
COPY --chown=irs_user:irs_user main.py .
COPY --chown=irs_user:irs_user .env.example .env

# Copy assets (data files, stopwords)
COPY --chown=irs_user:irs_user assets ./assets

# Create models directory (will be mounted as volume)
RUN mkdir -p models && chown -R irs_user:irs_user models

# Switch to non-root user
USER irs_user

# Expose API port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/', timeout=5)" || exit 1

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
