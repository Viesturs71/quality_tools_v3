"""
Script to clean all migration files except __init__.py
"""
import os
import shutil
import sys

def clean_migrations(app_name=None):
    """
    Delete all migration files except __init__.py for a specific app or all apps.
    
    Args:
        app_name (str, optional): The name of the app to clean migrations for.
            If None, clean migrations for all apps. Defaults to None.
    """
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    if app_name:
        apps = [app_name]
    else:
        # Get all directories that might be Django apps
        apps = [d for d in os.listdir(project_root) 
                if os.path.isdir(os.path.join(project_root, d))
                and not d.startswith('.') and not d == '__pycache__']
    
    print(f"Looking for migration files in the following apps: {', '.join(apps)}")
    
    total_removed = 0
    for app in apps:
        migrations_dir = os.path.join(project_root, app, 'migrations')
        
        if not os.path.exists(migrations_dir):
            print(f"No migrations directory found for app '{app}'")
            continue
            
        print(f"\nCleaning migrations for app: {app}")
        
        # Count files before deletion
        all_files = os.listdir(migrations_dir)
        migration_files = [f for f in all_files 
                          if f.endswith('.py') and f != '__init__.py']
        
        # Delete migration files
        for filename in migration_files:
            file_path = os.path.join(migrations_dir, filename)
            try:
                os.remove(file_path)
                print(f"Deleted: {filename}")
                total_removed += 1
            except Exception as e:
                print(f"Error deleting {filename}: {e}")
        
        # Ensure __init__.py exists
        init_file = os.path.join(migrations_dir, '__init__.py')
        if not os.path.exists(init_file):
            try:
                with open(init_file, 'w') as f:
                    f.write("# This file is required for Python to recognize this directory as a package")
                print("Created missing __init__.py file")
            except Exception as e:
                print(f"Error creating __init__.py: {e}")
    
    print(f"\nMigration cleanup complete. Removed {total_removed} migration files.")
    print("You should now run the following commands:")
    print("1. python manage.py makemigrations")
    print("2. python manage.py migrate")

if __name__ == "__main__":
    # Check if an app name was provided as a command-line argument
    if len(sys.argv) > 1:
        clean_migrations(sys.argv[1])
    else:
        clean_migrations()
