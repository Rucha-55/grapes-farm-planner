#!/bin/bash

# Exit on any error
set -e

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

# Start Gunicorn using Python module
exec python -m gunicorn.app.wsgiapp --config gunicorn_config.py app:app
