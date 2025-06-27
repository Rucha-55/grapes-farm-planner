# ========================================
# Builder stage
# ========================================
FROM python:3.9-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies in a specific order to avoid conflicts
RUN pip install --upgrade pip && \
    pip install --no-cache-dir setuptools==59.6.0 wheel==0.37.1 && \
    pip install --no-cache-dir numpy==1.23.5 && \
    pip install --no-cache-dir 'protobuf==3.19.6' --no-deps && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

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
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy from builder
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Create a non-root user and switch to it
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Create necessary directories with proper permissions
RUN mkdir -p /app/uploads /app/models && \
    chown -R appuser:appuser /app/uploads /app/models && \
    chmod 755 /app/uploads /app/models

# Download models during build (as root to ensure permissions)
USER root
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies needed for download_models
RUN pip install --no-cache-dir requests tqdm

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Run the download script with the current directory in Python path
RUN python -c "import os; print('Current directory:', os.getcwd()); print('Files in current directory:', os.listdir('.')); from download_models import download_models; download_models()"

# Verify models were downloaded
RUN echo "Verifying model files..." && \
    if [ ! -f "/app/models/grape_model.h5" ] || [ ! -f "/app/models/apple_disease.h5" ] || [ ! -f "/app/models/grape_leaf_disease_model.h5" ]; then \
        echo "Error: One or more model files are missing!" >&2; \
        ls -la /app/models/ || echo "Models directory not found"; \
        exit 1; \
    fi && \
    echo "All model files are present"

# Make start.sh executable
RUN chmod +x /app/start.sh

# Switch back to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE 10000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# Run the application
CMD ["./start.sh"]
