#!/bin/bash
# Exit on error
set -e

echo "🚀 Starting build process..."

# Check Python version
echo "🐍 Checking Python version..."
python3 --version

# Create virtual environment in the project directory
echo "🐍 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Upgrade pip and setuptools
echo "⬆️ Upgrading pip and setuptools..."
python -m pip install --upgrade pip==23.0.1 setuptools==65.5.0 wheel==0.38.4

# Set environment variables for TensorFlow
export TF_CPP_MIN_LOG_LEVEL=3
export TF_ENABLE_ONEDNN_OPTS=0

# Install specific versions of key dependencies first
echo "📦 Installing core dependencies..."
pip install numpy==1.24.3

# Install TensorFlow with specific version
echo "🤖 Installing TensorFlow..."
pip install tensorflow==2.10.1

# Install other requirements
echo "📋 Installing Python dependencies..."
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
