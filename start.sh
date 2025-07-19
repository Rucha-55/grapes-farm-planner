#!/bin/bash

# Exit on any error
set -e

# Print environment for debugging
echo "=== Environment Variables ==="
printenv
echo "============================"

# Set base directory
APP_DIR=$(pwd)
UPLOAD_DIR="$APP_DIR/uploads"
MODEL_DIR="$APP_DIR/models"

# Ensure uploads and models directories exist with proper permissions
echo "Setting up directories..."
mkdir -p "$UPLOAD_DIR"
mkdir -p "$MODEL_DIR"
chmod -R 755 "$UPLOAD_DIR"
chmod -R 755 "$MODEL_DIR"

# Check if model files exist
echo "Checking model files..."
for model in grape_model.h5 apple_disease.h5 grape_leaf_disease_model.h5; do
    if [ -f "$MODEL_DIR/$model" ]; then
        echo "Found model: $model"
        ls -lh "$MODEL_DIR/$model"
    else
        echo "WARNING: Model file not found: $model"
        # Create empty placeholder if file doesn't exist
        touch "$MODEL_DIR/$model"
    fi
done

# Find Python executable
PYTHON_EXECUTABLE=$(which python3 || which python)
echo "Using Python executable: $PYTHON_EXECUTABLE"

# Install gunicorn if not found
if ! command -v gunicorn &> /dev/null; then
    echo "Gunicorn not found. Installing..."
    $PYTHON_EXECUTABLE -m pip install gunicorn
fi

# Start Gunicorn using the config file
echo "Starting Gunicorn..."
if [ -f "gunicorn_config.py" ]; then
    echo "Using gunicorn_config.py"
    exec $PYTHON_EXECUTABLE -m gunicorn --config gunicorn_config.py app:app
else
    echo "gunicorn_config.py not found, using command line arguments"
    exec $PYTHON_EXECUTABLE -m gunicorn \
        --bind :$PORT \
        --workers 2 \
        --threads 4 \
        --worker-class gthread \
        --timeout 120 \
        --log-level debug \
        --access-logfile - \
        --error-logfile - \
        app:app
fi
