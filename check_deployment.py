#!/usr/bin/env python3
"""
Deployment Status Check Script
This script checks if all components are properly configured for Render deployment.
"""

import os
import sys
import importlib

def check_python_version():
    """Check Python version compatibility"""
    print("🐍 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Not compatible")
        return False

def check_required_files():
    """Check if all required files exist"""
    print("\n📁 Checking required files...")
    required_files = [
        'app.py',
        'requirements-minimal.txt',
        'render.yaml',
        'gunicorn_config.py',
        'start.sh'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - Missing")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_directories():
    """Check if required directories exist or can be created"""
    print("\n📂 Checking directories...")
    required_dirs = ['uploads', 'models', 'static/uploads']
    
    for dir_path in required_dirs:
        if os.path.exists(dir_path):
            print(f"✅ {dir_path}")
        else:
            try:
                os.makedirs(dir_path, exist_ok=True)
                print(f"✅ {dir_path} - Created")
            except Exception as e:
                print(f"❌ {dir_path} - Cannot create: {e}")
                return False
    return True

def check_syntax():
    """Check Python syntax"""
    print("\n🔍 Checking Python syntax...")
    try:
        import ast
        with open('app.py', 'r', encoding='utf-8') as f:
            ast.parse(f.read())
        print("✅ app.py - Syntax OK")
        return True
    except Exception as e:
        print(f"❌ app.py - Syntax error: {e}")
        return False

def check_imports():
    """Check if basic imports work"""
    print("\n📦 Checking basic imports...")
    try:
        import flask
        print("✅ Flask")
    except ImportError as e:
        print(f"❌ Flask: {e}")
        return False
    
    try:
        import numpy
        print("✅ NumPy")
    except ImportError as e:
        print(f"❌ NumPy: {e}")
        return False
    
    try:
        import pymongo
        print("✅ PyMongo")
    except ImportError as e:
        print(f"❌ PyMongo: {e}")
        return False
    
    return True

def main():
    """Main deployment check"""
    print("🚀 Render Deployment Status Check")
    print("=" * 50)
    
    checks = [
        check_python_version(),
        check_required_files(),
        check_directories(),
        check_syntax(),
        check_imports()
    ]
    
    print("\n" + "=" * 50)
    if all(checks):
        print("🎉 All checks passed! Ready for deployment.")
        print("\n📋 Next steps:")
        print("1. Commit changes to GitHub")
        print("2. Deploy to Render using Blueprint")
        print("3. Set environment variables in Render dashboard")
        return True
    else:
        print("❌ Some checks failed. Please fix issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 