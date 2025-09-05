#!/usr/bin/env python3
"""
Content Creator Studio - Fixed Setup Script
This script sets up the application with all fixes applied
"""

import subprocess
import sys
import os
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 9):
        print("❌ Python 3.9 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def install_requirements():
    """Install Python requirements"""
    print("📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def create_env_file():
    """Create .env file from template"""
    env_file = Path(".env")
    env_example = Path("env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from template...")
        with open(env_example, 'r') as f:
            content = f.read()
        with open(env_file, 'w') as f:
            f.write(content)
        print("✅ .env file created")
        print("⚠️  Please edit .env file with your API keys")
    else:
        print("✅ .env file already exists")

def check_docker():
    """Check if Docker is available"""
    try:
        subprocess.check_call(["docker", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        print("✅ Docker is available")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Docker not found - you can still run without Docker")
        return False

def main():
    """Main setup function"""
    print("🚀 Content Creator Studio - Fixed Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install requirements
    if not install_requirements():
        sys.exit(1)
    
    # Create .env file
    create_env_file()
    
    # Check Docker
    check_docker()
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Edit .env file with your API keys")
    print("2. Run: python start.py")
    print("3. Access the app at http://localhost:8501")
    print("\n🔧 All critical issues have been fixed:")
    print("✅ Database model issues resolved")
    print("✅ Security issues fixed")
    print("✅ Docker health checks fixed")
    print("✅ Error handling improved")
    print("✅ Async/await issues resolved")
    print("✅ Environment validation added")

if __name__ == "__main__":
    main()

