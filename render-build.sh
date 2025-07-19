#!/bin/bash
# Exit on error
set -e

echo "🚀 Starting build process..."

# Check if we're running in a container with read-only filesystem
if [ -w / ]; then
    # System is writable, install system dependencies
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
    
    # Create virtual environment in /opt/venv
    echo "🐍 Setting up Python virtual environment in /opt/venv..."
    python3 -m venv /opt/venv
    source /opt/venv/bin/activate
else
    # Running in read-only filesystem, use user space
    echo "🔧 Running in read-only filesystem, using user space..."
    # Create virtual environment in the project directory
    echo "🐍 Setting up Python virtual environment in project directory..."
    python3 -m venv venv
    source venv/bin/activate
fi

# Upgrade pip and setuptools
echo "⬆️ Upgrading pip and setuptools..."
pip install --upgrade pip setuptools wheel

# Set environment variables for TensorFlow
export TF_CPP_MIN_LOG_LEVEL=3
export TF_ENABLE_ONEDNN_OPTS=0

# Install specific versions of key dependencies first
echo "📦 Installing core dependencies..."
pip install --upgrade pip setuptools wheel
pip install numpy==1.26.4

# Install TensorFlow CPU first as it has specific requirements
echo "🤖 Installing TensorFlow CPU..."
pip install tensorflow-cpu==2.15.0

# Install other requirements
echo "📋 Installing Python dependencies..."
pip install -r requirements.txt --no-deps

# Install any missing dependencies
echo "🔍 Verifying all dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo "📂 Creating required directories..."
mkdir -p uploads

# Download models if needed
if [ -f "download_models.py" ]; then
    echo "⬇️ Downloading models (if needed)..."
    python download_models.py
else
    echo "ℹ️ No download_models.py found, skipping model download."
fi

echo "✅ Build completed successfully!"
