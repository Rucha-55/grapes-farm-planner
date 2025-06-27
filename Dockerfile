# ========================================
# Build stage
# ========================================
FROM python:3.9.18-slim as builder

# Set build arguments
ARG DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
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

# Create models directory and download models during build
RUN mkdir -p /app/models && \
    # Install required packages for model downloading
    pip install --no-cache-dir tqdm && \
    # Run the download script
    python -c "from download_models import download_models; download_models()" && \
    # Verify models were downloaded
    if [ ! -f "/app/models/grape_model.h5" ] || [ ! -f "/app/models/apple_disease.h5" ] || [ ! -f "/app/models/grape_leaf_disease_model.h5" ]; then \
        echo "Error: Failed to download one or more model files" >&2; \
        exit 1; \
    fi

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
    FLASK_APP=app.py \
    MODEL_DIR=/app/models

# Install runtime system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libhdf5-dev \
    libhdf5-serial-dev \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Create app directory and copy models from builder
WORKDIR /app
COPY --from=builder /app/models /app/models

# Verify models were copied correctly
RUN echo "Verifying model files..." && \
    if [ ! -f "/app/models/grape_model.h5" ] || [ ! -f "/app/models/apple_disease.h5" ] || [ ! -f "/app/models/grape_leaf_disease_model.h5" ]; then \
        echo "Error: One or more model files are missing in the runtime image" >&2; \
        exit 1; \
    fi && \
    echo "All model files are present"

# Copy the rest of the application
COPY --from=builder /app /app

# Install Python dependencies (without build dependencies)
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir gunicorn && \
    # Clean up pip cache
    rm -rf /root/.cache/pip/*

# Create a non-root user and switch to it
RUN useradd -m appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose the port the app runs on
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:10000", "app:app"]
