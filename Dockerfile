# ========================================
# Build stage
# ========================================
FROM python:3.9.18-slim as builder

# Set build arguments
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies in a specific order to avoid conflicts
RUN pip install --upgrade pip && \
    pip install --no-cache-dir setuptools==59.6.0 wheel==0.37.1 && \
    pip install --no-cache-dir numpy==1.23.5 && \
    pip install --no-cache-dir 'protobuf==3.19.6' --no-deps && \
    pip install --no-cache-dir gdown==4.6.6 && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Download models during build
RUN mkdir -p /app/models && \
    python -c "from download_models import download_models; download_models()"

# ========================================
# Runtime stage
# ========================================
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=10000 \
    TF_CPP_MIN_LOG_LEVEL=3 \
    TF_ENABLE_ONEDNN_OPTS=0 \
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

# Set work directory
WORKDIR /app

# Copy from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p uploads models && \
    chmod -R 755 uploads models

# Expose the port the app runs on
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# Command to run the application
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
