#!/bin/bash
# Exit on error
set -e

# Install system dependencies
apt-get update
apt-get install -y \
    python3-pip \
    python3-venv \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and setuptools
pip install --upgrade pip setuptools wheel

# Install specific versions of key dependencies first
pip install numpy==1.26.4
pip install tensorflow-cpu==2.15.0

# Now install the rest of the requirements
pip install -r requirements.txt

# Make sure the uploads directory exists
mkdir -p uploads

# Set permissions
chmod -R 755 .

echo "Setup completed successfully!"
