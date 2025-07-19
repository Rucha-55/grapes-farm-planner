#!/bin/bash

# Exit on any error
set -e

# Print environment for debugging
env

# Ensure uploads and models directories exist
mkdir -p uploads
mkdir -p models

# Set environment variables
export PYTHONPATH=$(pwd)

# Create placeholder model files if they don't exist
for model in grape_model.h5 apple_disease.h5 grape_leaf_disease_model.h5; do
    if [ ! -f "models/$model" ]; then
        echo "Creating placeholder for $model"
        touch "models/$model"
    fi
done

# Ensure proper permissions
chmod -R 755 uploads models

# Find Python and Gunicorn paths
PYTHON_PATH=$(which python3 || which python)
GUNICORN_PATH=$(which gunicorn || echo "gunicorn not found")

echo "Using Python: $PYTHON_PATH"
echo "Using Gunicorn: $GUNICORN_PATH"

# Try different ways to start Gunicorn
echo "Starting Gunicorn..."

exec $PYTHON_PATH -m gunicorn.app.wsgiapp \
  --bind :$PORT \
  --workers 2 \
  --threads 4 \
  --worker-class gthread \
  --timeout 120 \
  --log-level=debug \
  app:app
