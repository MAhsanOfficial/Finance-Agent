#!/usr/bin/env python3
"""
Startup script for Finance Agent FastAPI application
"""

import os
import sys
import subprocess
from pathlib import Path

def create_env_file():
    """Create a .env file with default values if it doesn't exist"""
    env_file = Path(".env")
    if not env_file.exists():
        print("Creating .env file with default values...")
        env_content = """# Database Configuration
# For PostgreSQL (uncomment and configure):
# DATABASE_URL=postgresql://username:password@localhost:5432/finance_db

# For SQLite (default, no configuration needed):
DATABASE_URL=sqlite:///./finance.db

# Gemini API Configuration (optional for agent functionality)
# GEMINI_API_KEY=your_gemini_api_key_here
"""
        with open(env_file, "w") as f:
            f.write(env_content)
        print("✅ Created .env file with default SQLite configuration")
    else:
        print("✅ .env file already exists")

def check_dependencies():
    """Check if required dependencies are installed"""
    try:
        import fastapi
        import sqlalchemy
        import uvicorn
        print("✅ Core dependencies are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing dependency: {e}")
        print("Please install dependencies with: pip install -r requirements.txt")
        return False

def main():
    print("🚀 Starting Finance Agent FastAPI Application")
    print("=" * 50)
    
    # Create .env file if it doesn't exist
    create_env_file()
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Start the application
    print("\n🌐 Starting FastAPI server...")
    print("📊 API Documentation will be available at: http://localhost:8000/docs")
    print("🔍 Health check endpoint: http://localhost:8000/health")
    print("💳 Payment data endpoint: http://localhost:8000/")
    print("\nPress Ctrl+C to stop the server")
    print("=" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n👋 Server stopped")

if __name__ == "__main__":
    main()
