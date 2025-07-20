#!/bin/bash

# Create necessary directories
mkdir -p uploads
mkdir -p models
mkdir -p static/uploads

# Create dummy model files if they don't exist
touch models/grape_model.h5
touch models/apple_disease.h5
touch models/grape_leaf_disease_model.h5
touch models/scaler.pkl
touch models/label_encoder.pkl

# Set environment variables
export FLASK_ENV=production
export PYTHONUNBUFFERED=1
export TF_CPP_MIN_LOG_LEVEL=3
export TF_ENABLE_ONEDNN_OPTS=0

# Start the application with sync workers
exec gunicorn --bind :$PORT --workers 2 --threads 4 --worker-class sync --timeout 120 --log-level=info app:app
