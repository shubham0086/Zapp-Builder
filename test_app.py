#!/usr/bin/env python3
"""
Test script to verify application can start
"""

import sys
import os
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))
sys.path.insert(0, str(current_dir / "backend"))

def test_imports():
    """Test if all imports work correctly"""
    try:
        print("Testing imports...")
        
        # Test core imports
        from backend.core.config import settings
        print("✅ Config imported successfully")
        
        from backend.api.models import User, Project, ContentDraft
        print("✅ Models imported successfully")
        
        from backend.api.routes import router
        print("✅ Routes imported successfully")
        
        from backend.main import app
        print("✅ Main app imported successfully")
        
        print("\n🎉 All imports successful!")
        return True
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_backend_start():
    """Test if backend can start"""
    try:
        print("\nTesting backend startup...")
        from backend.main import app
        
        # Test if app is properly configured
        if hasattr(app, 'routes'):
            print("✅ FastAPI app configured successfully")
            print(f"✅ App title: {app.title}")
            print(f"✅ App version: {app.version}")
            return True
        else:
            print("❌ FastAPI app not properly configured")
            return False
            
    except Exception as e:
        print(f"❌ Backend startup error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Testing Content Creator Studio Application")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        return False
    
    # Test backend startup
    if not test_backend_start():
        print("\n❌ Backend startup tests failed")
        return False
    
    print("\n🎉 All tests passed! Application is ready to run.")
    print("\n📋 Next steps:")
    print("1. Run: python run_app.py")
    print("2. Access frontend at: http://localhost:8501")
    print("3. Access backend API at: http://localhost:8000")
    print("4. View API docs at: http://localhost:8000/docs")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
