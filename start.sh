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
    fi
done

# Start Gunicorn
echo "Starting Gunicorn..."
exec gunicorn \
    --bind :$PORT \
    --workers 2 \
    --threads 4 \
    --worker-class gthread \
    --timeout 120 \
    --log-level=debug \
    --access-logfile - \
    --error-logfile - \
    app:app
