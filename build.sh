#!/bin/bash
set -e

# Set Python version
export PYTHONUNBUFFERED=1

# Upgrade pip
python -m pip install --upgrade pip==21.3.1

# Install system dependencies
apt-get update
apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies with specific versions
pip install --no-cache-dir \
    numpy==1.22.4 \
    h5py==3.6.0 \
    protobuf==3.20.3

# Install the rest of the requirements
pip install --no-cache-dir -r requirements.txt

# Create necessary directories
mkdir -p uploads

# Set permissions
chmod -R 755 .

echo "Build completed successfully!"
