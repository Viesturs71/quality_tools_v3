#!/usr/bin/env python
"""
Script to safely restart Django development server
with cache clearing and proper reload.
"""
import os
import shutil
import subprocess
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def clear_cache_files():
    """Clear Python bytecode cache files."""
    print("Clearing cache files...")
    
    # Recursively remove all __pycache__ directories
    for pycache_dir in BASE_DIR.glob('**/__pycache__'):
        if pycache_dir.is_dir():
            shutil.rmtree(pycache_dir)
            print(f"Removed: {pycache_dir}")
    
    # Also remove .pyc files
    for pyc_file in BASE_DIR.glob('**/*.pyc'):
        if pyc_file.is_file():
            pyc_file.unlink()
            print(f"Removed: {pyc_file}")

def restart_server():
    """Restart Django development server with proper flags."""
    print("\nRestarting Django server...\n")
    
    # Use --noreload flag to disable Django's auto-reloader
    # Use --nothreading for single-threaded operation to avoid caching issues
    subprocess.run([
        "python", "manage.py", "runserver",
        "--noreload", "--nothreading"
    ])

if __name__ == "__main__":
    clear_cache_files()
    restart_server()
