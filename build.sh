#!/bin/bash
set -e

# Upgrade pip
python -m pip install --upgrade pip

# Install system dependencies
apt-get update
apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
mkdir -p uploads

# Set permissions
chmod -R 755 .

echo "Build completed successfully!"
