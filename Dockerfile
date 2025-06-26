# Build stage
FROM python:3.9.18-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies with specific versions first
COPY requirements.txt .

# Install pip and setuptools first with specific versions
RUN pip install --upgrade pip==23.1.2 setuptools==65.5.0 wheel==0.40.0

# Install numpy first as it's a common dependency with specific version requirements
RUN pip install --no-cache-dir numpy==1.23.5

# Install protobuf first to avoid conflicts
RUN pip install --no-cache-dir 'protobuf==3.19.6' --no-deps

# Now install the rest of the requirements
RUN pip install --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.9.18-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PORT=10000 \
    TF_CPP_MIN_LOG_LEVEL=3 \
    TF_ENABLE_ONEDNN_OPTS=0 \
    PYTHONPATH=/app \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR /app

# Install runtime dependencies
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

# Copy application code
COPY . .

# Create necessary directories and set permissions
RUN mkdir -p uploads && \
    chmod -R 755 .

# Expose the port the app runs on
EXPOSE 10000

# Command to run the application
CMD ["gunicorn", "--config", "gunicorn_config.py", "app:app"]
