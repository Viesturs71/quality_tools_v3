"""
Script to reset migrations for all apps in the project.
This will ensure a clean migration process for all applications.
"""
import os
import shutil
import datetime
import sys
import subprocess

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def simple_migration_reset(backup=True):
    """
    Reset migrations for all apps without using Django setup.
    
    Args:
        backup (bool): Whether to backup migrations before deleting
    """
    print("Starting migration reset for all apps...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create backup directory if needed
    if backup:
        backup_dir = os.path.join(BASE_DIR, f'migrations_backup_{timestamp}')
        os.makedirs(backup_dir, exist_ok=True)
        print(f"Created backup directory: {backup_dir}")
    
    # Find and process migration files
    deleted_count = 0
    backed_up_count = 0
    
    for root, dirs, files in os.walk(BASE_DIR):
        # Check if this is a migrations directory
        if os.path.basename(root) == 'migrations':
            app_name = os.path.basename(os.path.dirname(root))
            migration_files = [f for f in files if f.endswith('.py') and f != '__init__.py']
            
            # Backup migrations if enabled
            if backup and migration_files:
                app_backup_dir = os.path.join(backup_dir, app_name, 'migrations')
                os.makedirs(app_backup_dir, exist_ok=True)
                
                for file in migration_files:
                    src_path = os.path.join(root, file)
                    dst_path = os.path.join(app_backup_dir, file)
                    try:
                        shutil.copy2(src_path, dst_path)
                        backed_up_count += 1
                    except Exception as e:
                        print(f"Error backing up {src_path}: {str(e)}")
            
            # Delete migration files
            for file in migration_files:
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    deleted_count += 1
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Error deleting {file_path}: {str(e)}")
    
    print(f"\nDeleted {deleted_count} migration files while preserving __init__.py files.")
    
    if backup and backed_up_count > 0:
        print(f"Backed up {backed_up_count} migration files to: {backup_dir}")
        print("To restore, copy the files back to their respective migrations folders.")

def ensure_init_files_exist():
    """Ensure all migrations directories have an __init__.py file."""
    created_count = 0
    for root, dirs, files in os.walk(BASE_DIR):
        # Check if this is a migrations directory
        if os.path.basename(root) == 'migrations':
            init_file = os.path.join(root, '__init__.py')
            if not os.path.exists(init_file):
                try:
                    # Create empty __init__.py file
                    with open(init_file, 'w') as f:
                        pass
                    created_count += 1
                    print(f"Created missing __init__.py in: {root}")
                except Exception as e:
                    print(f"Error creating __init__.py in {root}: {str(e)}")
    
    print(f"Created {created_count} missing __init__.py files.")

def check_migrations_status():
    """Print information about existing migrations."""
    migration_count = 0
    init_missing_count = 0
    
    print("\nChecking migrations status...")
    
    app_stats = {}
    
    for root, dirs, files in os.walk(BASE_DIR):
        if os.path.basename(root) == 'migrations':
            app_name = os.path.basename(os.path.dirname(root))
            migration_files = [f for f in files if f.endswith('.py') and f != '__init__.py']
            
            # Check if __init__.py exists
            has_init = '__init__.py' in files
            
            if not has_init:
                init_missing_count += 1
            
            migration_count += len(migration_files)
            app_stats[app_name] = {
                'count': len(migration_files),
                'has_init': has_init,
                'path': root
            }
    
    # Print results in a sorted manner
    for app_name in sorted(app_stats.keys()):
        stats = app_stats[app_name]
        print(f"{app_name}: {stats['count']} migration(s)" + 
              ("" if stats['has_init'] else " (missing __init__.py)"))
    
    print(f"\nTotal: {migration_count} migration files found across {len(app_stats)} apps")
    if init_missing_count > 0:
        print(f"Warning: {init_missing_count} migrations directories are missing __init__.py")

if __name__ == "__main__":
    print("=================== MIGRATION RESET TOOL ===================")
    print("This script will delete all migration files except __init__.py.")
    print("WARNING: This is a destructive operation and should only be used in development.")
    print("\nOptions:")
    print("1. Remove all migration files (keep __init__.py)")
    print("2. Check migrations status")
    print("3. Ensure all migrations folders have __init__.py")
    print("q. Quit")
    
    choice = input("\nEnter your choice (1-3, q): ").lower()
    
    if choice == '1':
        confirm = input("Are you sure you want to delete all migration files? (y/n): ").lower()
        if confirm == 'y':
            backup = input("Create backup of migrations before deleting? (y/n): ").lower() == 'y'
            simple_migration_reset(backup=backup)
            print("Migration files deletion completed.")
        else:
            print("Operation cancelled.")
    
    elif choice == '2':
        check_migrations_status()
    
    elif choice == '3':
        ensure_init_files_exist()
    
    elif choice == 'q':
        print("Exiting migration tool.")
    
    else:
        print("Invalid choice. Exiting.")
