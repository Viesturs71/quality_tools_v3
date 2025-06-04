#!/usr/bin/env python
"""
File monitoring and diagnostic tool for Django project.
"""
import hashlib
import os
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

def get_file_hash(file_path):
    """Generate MD5 hash for a file to track changes."""
    if not os.path.exists(file_path):
        return None
    try:
        with open(file_path, 'rb') as f:
            return hashlib.md5(f.read()).hexdigest()
    except Exception as e:
        return f"Error: {str(e)}"

def monitor_directory(directory, extensions=None, interval=2):
    """Monitor all files in a directory for changes."""
    print(f"Monitoring directory: {directory}")
    if extensions:
        print(f"File types: {', '.join(extensions)}")
    
    file_hashes = {}
    
    # Initial file scan
    for root, _, files in os.walk(directory):
        for file in files:
            if extensions and not any(file.endswith(ext) for ext in extensions):
                continue
                
            file_path = os.path.join(root, file)
            file_hashes[file_path] = get_file_hash(file_path)
    
    print(f"Monitoring {len(file_hashes)} files. Press Ctrl+C to stop...")
    
    try:
        while True:
            time.sleep(interval)
            for file_path, old_hash in list(file_hashes.items()):
                # Check if file still exists
                if not os.path.exists(file_path):
                    print(f"File deleted: {file_path}")
                    del file_hashes[file_path]
                    continue
                    
                # Check for changes
                new_hash = get_file_hash(file_path)
                if new_hash != old_hash:
                    print(f"File changed: {file_path}")
                    file_hashes[file_path] = new_hash
            
            # Check for new files
            for root, _, files in os.walk(directory):
                for file in files:
                    if extensions and not any(file.endswith(ext) for ext in extensions):
                        continue
                        
                    file_path = os.path.join(root, file)
                    if file_path not in file_hashes:
                        print(f"New file: {file_path}")
                        file_hashes[file_path] = get_file_hash(file_path)
                    
    except KeyboardInterrupt:
        print("\nMonitoring stopped.")

if __name__ == "__main__":
    # Monitorēt templates direktoriju
    templates_dir = os.path.join(BASE_DIR, "templates")
    monitor_directory(templates_dir, extensions=['.html'])
