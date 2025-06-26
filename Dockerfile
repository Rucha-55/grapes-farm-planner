# ========================================
# Build stage
# ========================================
FROM python:3.9.18-slim as builder

# Set build arguments
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install pip and setuptools with specific versions
RUN pip install --no-cache-dir --upgrade pip==23.1.2 setuptools==65.5.0 wheel==0.40.0

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies in a specific order to avoid conflicts
RUN pip install --no-cache-dir numpy==1.23.5 && \
    pip install --no-cache-dir 'protobuf==3.19.6' --no-deps && \
    pip install --no-cache-dir -r requirements.txt && \
    pip install gdown==4.7.1

# Download models during build
RUN mkdir -p /app/models
RUN python -c "from download_models import download_models; download_models()"

# ========================================
# Runtime stage
# ========================================
FROM python:3.9.18-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=10000 \
    TF_CPP_MIN_LOG_LEVEL=3 \
    TF_ENABLE_ONEDNN_OPTS=0 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    FLASK_ENV=production \
    FLASK_APP=app.py

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    libgl1 \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Set working directory
WORKDIR /app

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p uploads && \
    chmod -R 755 /app/uploads

# Expose the port the app runs on
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# Command to run the application
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
