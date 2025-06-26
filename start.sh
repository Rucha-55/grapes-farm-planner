#!/bin/bash

# Exit on any error
set -e

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Set permissions
chmod -R 755 uploads

# Set environment variables
export PYTHONPATH=/app

# Start Gunicorn
exec gunicorn --config gunicorn_config.py app:app
