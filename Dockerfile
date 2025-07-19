FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    PORT=10000 \
    PATH="/home/appuser/.local/bin:$PATH" \
    TF_CPP_MIN_LOG_LEVEL=3 \
    TF_ENABLE_ONEDNN_OPTS=0 \
    FLASK_ENV=production \
    FLASK_APP=app.py \
    DEBIAN_FRONTEND=noninteractive

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libgl1-mesa-glx \
    libglib2.0-0 \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create appuser and set up directories
RUN useradd -m appuser && \
    mkdir -p /app/uploads /app/models && \
    chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY --chown=appuser:appuser requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Download model files using direct links with wget
RUN cd /app/models && \
    wget -q --show-progress --progress=bar:force:noscrape -O grape_model.h5 "https://drive.google.com/uc?export=download&id=1xFJROCP69sNcH0E4TdD38OvSdIJUalGC" && \
    wget -q --show-progress --progress=bar:force:noscrape -O apple_disease.h5 "https://drive.google.com/uc?export=download&id=1HjIVeMdsnW40n3IMLUp1r68PmmVsrSFX" && \
    wget -q --show-progress --progress=bar:force:noscrape -O grape_leaf_disease_model.h5 "https://drive.google.com/uc?export=download&id=1dzGkGnDyC7yXKER1Q2X8z0ycDMWY1SQ3" && \
    wget -q --show-progress --progress=bar:force:noscrape -O scaler.pkl "https://drive.google.com/uc?export=download&id=1cFdAGQAkYUjtLRpsRO8pyEfmZ9IPV9eY" && \
    wget -q --show-progress --progress=bar:force:noscrape -O label_encoder.pkl "https://drive.google.com/uc?export=download&id=14C9YCEts3Lza3iGHSnhrApN29JsqIJQU" && \
    chown -R appuser:appuser /app/models

# Copy the rest of the application
COPY --chown=appuser:appuser . .

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

# Switch to non-root user
USER appuser

# Expose the port the app runs on
EXPOSE $PORT

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:10000/health || exit 1

# Run the application
CMD ["./start.sh"]
