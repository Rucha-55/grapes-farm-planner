#!/bin/bash

# Exit on any error
set -e

# Ensure uploads directory exists (should be created in Dockerfile)
if [ ! -d "uploads" ]; then
    mkdir -p uploads
fi

# Set environment variables
export PYTHONPATH=/app

# Start Gunicorn
exec gunicorn --config gunicorn_config.py app:app
