#!/usr/bin/env python3
"""
Test script to verify backend functionality
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
        
        from backend.core.database import create_tables
        print("✅ Database module imported successfully")
        
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

def test_database():
    """Test database table creation"""
    try:
        print("\nTesting database...")
        # Clear any existing metadata to avoid conflicts
        from backend.core.database import Base
        Base.metadata.clear()
        
        from backend.core.database import create_tables
        create_tables()
        print("✅ Database tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main test function"""
    print("🧪 Testing Content Creator Studio Backend")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("\n❌ Import tests failed")
        return False
    
    # Test database
    if not test_database():
        print("\n❌ Database tests failed")
        return False
    
    print("\n🎉 All tests passed! Backend is ready to run.")
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

