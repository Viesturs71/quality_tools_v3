"""
Script to delete all migration files except for __init__.py in each app's migrations directory.
This helps reset the migration state when you need to start fresh.

Usage:
    python delete_migrations.py
"""

import os
from pathlib import Path

# Get the base directory of the Django project
BASE_DIR = Path(__file__).resolve().parent

# List of apps to process
APPS = [
    'accounts',
    'equipment',
    'documents',
    'personnel',
    'dashboard',
    'company',
    'standards',
    'companies',
    'methods'
]

def delete_migrations():
    """Delete all migration files except for __init__.py in each app's migrations directory."""
    total_deleted = 0
    
    print("Searching for migration files to delete...")
    
    for app in APPS:
        app_path = BASE_DIR / app
        migrations_path = app_path / 'migrations'
        
        if not migrations_path.exists():
            print(f"Migrations directory for {app} does not exist. Skipping.")
            continue
        
        # Count migration files before deletion
        migration_files = [
            f for f in os.listdir(migrations_path) 
            if f.endswith('.py') and f != '__init__.py'
        ]
        
        file_count = len(migration_files)
        
        if file_count == 0:
            print(f"No migration files found in {app}. Skipping.")
            continue
        
        print(f"Found {file_count} migration files in {app}.")
        
        # Delete migration files
        for file_name in migration_files:
            file_path = migrations_path / file_name
            os.remove(file_path)
            print(f"  Deleted: {file_path}")
            total_deleted += 1
        
        # Make sure __init__.py exists
        init_file = migrations_path / '__init__.py'
        if not init_file.exists():
            with open(init_file, 'w') as f:
                f.write('# This file is required for Django to recognize this directory as a package\n')
            print(f"  Created: {init_file}")
    
    # Print summary
    print(f"\nDeletion complete. Removed {total_deleted} migration files.")
    print("Remember to reset your database or run `python manage.py migrate` with the `--fake` option if needed.")

if __name__ == "__main__":
    # Ask for confirmation
    confirm = input("This will delete all migration files except __init__.py. Continue? (y/n): ")
    if confirm.lower() == 'y':
        delete_migrations()
    else:
        print("Operation cancelled.")
