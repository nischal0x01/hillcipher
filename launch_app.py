#!/usr/bin/env python3
"""
Launch script for the Hill Cipher Streamlit application
"""

import subprocess
import sys
import os

def main():
    """
    Launch the Streamlit application
    """
    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Path to the virtual environment python
    venv_python = os.path.join(script_dir, '.venv', 'bin', 'python')
    
    # Path to the app.py file
    app_path = os.path.join(script_dir, 'app.py')
    
    # Check if virtual environment exists
    if not os.path.exists(venv_python):
        print("❌ Virtual environment not found!")
        print("Please run the following commands to set up the environment:")
        print("  python -m venv .venv")
        print("  source .venv/bin/activate")
        print("  pip install -r requirements.txt")
        return
    
    # Check if app.py exists
    if not os.path.exists(app_path):
        print("❌ app.py not found!")
        return
    
    print("🚀 Starting Hill Cipher Streamlit Application...")
    print("📱 The app will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Launch streamlit
        subprocess.run([
            venv_python, '-m', 'streamlit', 'run', app_path,
            '--server.headless=false',
            '--server.port=8501',
            '--server.runOnSave=true'
        ])
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")
        print("Try running manually: streamlit run app.py")

if __name__ == "__main__":
    main()
