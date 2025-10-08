#!/usr/bin/env python3
"""
Startup script for Gradient Lab Color Gradient Generator
"""

import os
import sys
import subprocess

def main():
    # Change to backend directory
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    os.chdir(backend_dir)
    
    print("🎨 Starting Gradient Lab Color Gradient Generator...")
    print("📁 Project structure:")
    print("   - Frontend: ../frontend/")
    print("   - Backend:  ./backend/")
    print()
    
    # Start the server
    try:
        import uvicorn
        print("🚀 Starting server at http://127.0.0.1:8000")
        print("📚 API Documentation: http://127.0.0.1:8000/api/docs")
        print("🧪 Test page: http://127.0.0.1:8000/test")
        print()
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
    except ImportError:
        print("❌ uvicorn not found. Please install requirements:")
        print("   pip install -r requirements.txt")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        return 0

if __name__ == '__main__':
    sys.exit(main())