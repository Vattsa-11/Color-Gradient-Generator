#!/usr/bin/env python3
"""
Startup script for Gradient Lab Color Gradient Generator
"""

import os
import sys
import subprocess

def main():
    # Get the project root directory
    project_root = os.path.dirname(__file__)
    backend_dir = os.path.join(project_root, 'backend')
    
    # Verify backend directory exists
    if not os.path.exists(backend_dir):
        print("❌ Backend directory not found!")
        print(f"Expected: {backend_dir}")
        return 1
    
    # Verify server.py exists
    server_file = os.path.join(backend_dir, 'server.py')
    if not os.path.exists(server_file):
        print("❌ server.py not found in backend directory!")
        print(f"Expected: {server_file}")
        return 1
    
    print("🎨 Starting Gradient Lab Color Gradient Generator...")
    print("📁 Project structure:")
    print(f"   - Frontend: {os.path.join(project_root, 'frontend')}")
    print(f"   - Backend:  {backend_dir}")
    print()
    
    # Add backend directory to Python path
    sys.path.insert(0, backend_dir)
    
    # Change to backend directory for uvicorn
    original_cwd = os.getcwd()
    os.chdir(backend_dir)
    
    # Start the server
    try:
        import uvicorn
        print("🚀 Starting server at http://127.0.0.1:8000")
        print("📚 API Documentation: http://127.0.0.1:8000/api/docs")
        print("🧪 Test page: http://127.0.0.1:8000/test")
        print()
        print("Press Ctrl+C to stop the server")
        print("-" * 50)
        
        # Run the server with proper module path
        uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please install requirements:")
        print(f"   cd {backend_dir}")
        print("   pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return 1
    except KeyboardInterrupt:
        print("\n👋 Server stopped")
        return 0
    finally:
        # Restore original working directory
        os.chdir(original_cwd)

if __name__ == '__main__':
    sys.exit(main())