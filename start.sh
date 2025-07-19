#!/bin/bash

# Exit on any error
set -e

# Print environment for debugging
echo "=== Environment Variables ==="
printenv
echo "============================"

# Ensure uploads directory exists with proper permissions
echo "Setting up directories..."
mkdir -p /app/uploads
chmod -R 755 /app/uploads

# Check if model files exist
echo "Checking model files..."
for model in grape_model.h5 apple_disease.h5 grape_leaf_disease_model.h5; do
    if [ -f "/app/models/$model" ]; then
        echo "Found model: $model"
        ls -lh "/app/models/$model"
    else
        echo "WARNING: Model file not found: $model"
        # Create empty placeholder if file doesn't exist
        touch "/app/models/$model"
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
echo "Starting Gunicorn with config file..."
if [ -f "/app/gunicorn_config.py" ]; then
    echo "Using gunicorn_config.py"
    exec $PYTHON_EXECUTABLE -m gunicorn --config /app/gunicorn_config.py app:app
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
