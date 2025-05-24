# Financial Risk Assessment System Docker Configuration
# Multi-stage build for optimized production image

# Build stage
FROM python:3.11-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libx11-dev \
    libxext-dev \
    libxrender-dev \
    libxtst6 \
    libxi6 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libfontconfig1 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy requirements and install Python dependencies
COPY requirements.txt /tmp/
RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

# Production stage
FROM python:3.11-slim as production

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH" \
    FLASK_ENV=production \
    DB_TYPE=postgres

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
    libpq5 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxtst6 \
    libxi6 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libfontconfig1 \
    libdbus-1-3 \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN groupadd -r finance && useradd --no-log-init -r -g finance finance

# Copy virtual environment from builder stage
COPY --from=builder /opt/venv /opt/venv

# Create application directory
WORKDIR /app

# Copy application code
COPY project\ code/ ./project\ code/
COPY requirements.txt .
COPY README.md .
COPY setup.cfg .

# Create necessary directories
RUN mkdir -p logs models backups && \
    chown -R finance:finance /app

# Copy startup script
COPY docker/start.sh /start.sh
RUN chmod +x /start.sh && chown finance:finance /start.sh

# Switch to non-root user
USER finance

# Expose port
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1

# Default command
CMD ["/start.sh"] 