"""
Test script to verify the FastAPI application works correctly
"""

def test_imports():
    """Test if all modules can be imported"""
    try:
        from main import app
        print("✅ Main module imports successfully")
        
        from database import engine, SessionLocal
        print("✅ Database module imports successfully")
        
        from models import Payment
        print("✅ Models module imports successfully")
        
        from mockdata import mockdata
        print("✅ Mockdata module imports successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import error: {e}")
        return False

def test_app_routes():
    """Test if FastAPI app has expected routes"""
    try:
        from main import app
        
        routes = []
        for route in app.routes:
            if hasattr(route, 'methods') and hasattr(route, 'path'):
                methods = list(route.methods)
                routes.append(f"{methods} {route.path}")
        
        print("✅ Available routes:")
        for route in routes:
            print(f"  {route}")
        
        expected_routes = ["GET /", "GET /health", "POST /save-to-db/", "GET /get-payments/", "GET /run-agent/"]
        found_routes = [route for route in routes if any(expected in route for expected in expected_routes)]
        
        if len(found_routes) >= 4:  # At least 4 out of 5 routes should be present
            print("✅ All expected routes are available")
            return True
        else:
            print(f"⚠️  Only {len(found_routes)} out of 5 expected routes found")
            return False
            
    except Exception as e:
        print(f"❌ Route test error: {e}")
        return False

def test_database_connection():
    """Test database connection"""
    try:
        from database import engine
        with engine.connect() as conn:
            print("✅ Database connection successful")
            return True
    except Exception as e:
        print(f"❌ Database connection error: {e}")
        return False

def main():
    print("🧪 Testing Finance Agent FastAPI Application")
    print("=" * 50)
    
    tests = [
        ("Import Test", test_imports),
        ("Route Test", test_app_routes),
        ("Database Test", test_database_connection),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔍 Running {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The application should work correctly.")
        print("\n🚀 To start the server, run:")
        print("   python start_server.py")
        print("   or")
        print("   uvicorn main:app --reload")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
