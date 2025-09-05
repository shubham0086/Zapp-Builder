#!/usr/bin/env python3
"""
Content Creator Studio - Startup Script
Run this to start the application in development mode
"""

import subprocess
import sys
import os
import time
from pathlib import Path

def check_requirements():
    """Check if requirements are installed"""
    try:
        import streamlit
        import fastapi
        import uvicorn
        print("✅ All requirements are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing requirement: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting backend server...")
    backend_dir = Path("backend")
    if backend_dir.exists():
        os.chdir(backend_dir)
        subprocess.Popen([sys.executable, "-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "8000"])
        os.chdir("..")
        print("✅ Backend started on http://localhost:8000")
    else:
        print("❌ Backend directory not found")

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting frontend application...")
    time.sleep(2)  # Give backend time to start
    
    frontend_dir = Path("frontend")
    if frontend_dir.exists():
        os.chdir(frontend_dir)
        subprocess.run([sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.port=8501"])
    else:
        print("❌ Frontend directory not found")

def main():
    """Main startup function"""
    print("🎯 Content Creator Studio - Development Mode")
    print("=" * 50)
    
    # Check requirements
    if not check_requirements():
        sys.exit(1)
    
    # Check for .env file
    if not Path(".env").exists():
        print("⚠️  No .env file found. Copy env.example to .env and configure your API keys")
        print("   cp env.example .env")
    
    print("\n🚀 Starting services...")
    print("   Backend: http://localhost:8000")
    print("   Frontend: http://localhost:8501")
    print("   API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Start backend in background
        start_backend()
        
        # Start frontend (this will block)
        start_frontend()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down services...")
        sys.exit(0)

if __name__ == "__main__":
    main()

