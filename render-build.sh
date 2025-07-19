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

# Install core dependencies with specific versions
echo "📦 Installing core dependencies..."
pip install --upgrade pip==23.0.1
pip install setuptools==65.5.0 wheel==0.38.4

# Install protobuf first with specific version
pip install protobuf==3.19.5

# Install TensorFlow and its dependencies
echo "🤖 Installing TensorFlow and ML dependencies..."
pip install tensorflow-cpu==2.10.1
pip install keras==2.10.0
pip install tensorboard==2.10.1
pip install numpy==1.23.5

# Install gunicorn and gevent
pip install gunicorn==20.1.0 gevent==21.12.0

# Install other requirements
echo "📋 Installing remaining Python dependencies..."
pip install -r requirements.txt --no-deps

# Now install all dependencies with dependency resolution
pip install -r requirements.txt

# Create necessary directories
echo "📂 Creating required directories..."
mkdir -p uploads

# Create models directory
mkdir -p models

# Skip model downloads for now
# The models should be included in the repository or provided separately
echo "⚠️  Skipping model downloads. Please ensure models are included in the repository."

# Create placeholder files if they don't exist
for model in grape_model.h5 apple_disease.h5 grape_leaf_disease_model.h5; do
    if [ ! -f "models/$model" ]; then
        echo "ℹ️  Creating placeholder for $model"
        touch "models/$model"
    fi
done

echo "✅ Build completed successfully!"
