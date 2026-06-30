#!/usr/bin/env python3
"""
Simple API launcher for TrueSight system
"""
import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Import and run the API
from src.api.main import app
import uvicorn

if __name__ == "__main__":
    print("🚀 Starting TrueSight API Server...")
    print("🌐 API will be available at http://localhost:8000")
    print("📝 Documentation at http://localhost:8000/docs")
    print("🔄 Press Ctrl+C to stop the server")
    print("=" * 50)
    
    uvicorn.run(
        "src.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )