#!/usr/bin/env python3
"""
Content Creator Studio - Fixed Startup Script
This script properly sets up the Python path and starts the application
"""

import sys
import os
import subprocess
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "backend"))

def check_dependencies():
    """Check if all required dependencies are installed"""
    try:
        import streamlit
        import fastapi
        import uvicorn
        print("✅ All core dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        return False

def start_backend():
    """Start the FastAPI backend"""
    print("🚀 Starting backend server...")
    try:
        # Change to backend directory and start uvicorn
        backend_dir = current_dir / "backend"
        os.chdir(backend_dir)
        
        # Start uvicorn with proper module path
        subprocess.Popen([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--reload", 
            "--host", "0.0.0.0", 
            "--port", "8000"
        ])
        
        print("✅ Backend started on http://localhost:8000")
        return True
    except Exception as e:
        print(f"❌ Failed to start backend: {e}")
        return False

def start_frontend():
    """Start the Streamlit frontend"""
    print("🎨 Starting frontend application...")
    try:
        # Change to frontend directory
        frontend_dir = current_dir / "frontend"
        os.chdir(frontend_dir)
        
        # Start streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", 
            "run", "streamlit_app.py", 
            "--server.port=8501"
        ])
    except Exception as e:
        print(f"❌ Failed to start frontend: {e}")

def main():
    """Main startup function"""
    print("🎯 Content Creator Studio - Fixed Version")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("Please install dependencies first: pip install -r requirements.txt")
        return
    
    # Check for .env file
    env_file = current_dir / ".env"
    if not env_file.exists():
        print("⚠️  No .env file found. Creating from template...")
        env_example = current_dir / "env.example"
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("✅ .env file created from template")
        else:
            print("❌ No env.example file found")
    
    print("\n🚀 Starting services...")
    print("   Backend: http://localhost:8000")
    print("   Frontend: http://localhost:8501")
    print("   API Docs: http://localhost:8000/docs")
    print("\nPress Ctrl+C to stop all services")
    
    try:
        # Start backend
        if start_backend():
            # Wait a moment for backend to start
            import time
            time.sleep(3)
            
            # Start frontend (this will block)
            start_frontend()
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down services...")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()

