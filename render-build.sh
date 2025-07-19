#!/bin/bash
# Exit on error
set -e

echo "🚀 Starting build process..."

# Install system dependencies
echo "🔧 Installing system dependencies..."
apt-get update
apt-get install -y \
    python3-pip \
    python3-venv \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Create and activate virtual environment
echo "🐍 Setting up Python virtual environment..."
python3 -m venv /opt/venv
source /opt/venv/bin/activate

# Upgrade pip and setuptools
echo "⬆️ Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Install specific versions of key dependencies first
echo "📦 Installing core dependencies..."
pip install numpy==1.26.4
export TF_CPP_MIN_LOG_LEVEL=3
export TF_ENABLE_ONEDNN_OPTS=0

# Install requirements
echo "📋 Installing Python dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📂 Creating required directories..."
mkdir -p uploads

# Download models if needed
echo "⬇️ Downloading models (if needed)..."
python download_models.py

echo "✅ Build completed successfully!"
