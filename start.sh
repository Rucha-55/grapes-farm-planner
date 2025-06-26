#!/bin/bash

# Create uploads directory if it doesn't exist
mkdir -p uploads

# Set permissions
chmod -R 755 .


# Start the application
exec gunicorn --config gunicorn_config.py app:app
