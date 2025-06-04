"""
Script to clean up accounts app migrations specifically.
This is a safer approach than resetting all migrations.
"""
import os
import shutil
import django
from django.db import connection
import datetime

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def clean_accounts_migrations():
    """Clean up conflicting migrations in the accounts app."""
    print("Starting cleanup of accounts app migrations...")
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    
    # Create backup directory
    backup_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                             f'accounts_migrations_backup_{timestamp}')
    os.makedirs(backup_dir, exist_ok=True)
    print(f"Created backup directory: {backup_dir}")
    
    # Path to accounts migrations
    accounts_migrations_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                         'accounts', 'migrations')
    
    # Backup and delete problematic migrations
    migration_files = [f for f in os.listdir(accounts_migrations_dir) 
                      if f.endswith('.py') and f != '__init__.py'
                      and f != '0001_initial.py']  # Keep initial migration
    
    # Backup migrations
    for file in migration_files:
        src_path = os.path.join(accounts_migrations_dir, file)
        dst_path = os.path.join(backup_dir, file)
        shutil.copy2(src_path, dst_path)
        print(f"Backed up: {file}")
    
    # Delete conflicting migrations
    for file in migration_files:
        if any(x in file for x in ['fix_department', 'ensure_department', 'remove_and_readd']):
            file_path = os.path.join(accounts_migrations_dir, file)
            os.remove(file_path)
            print(f"Deleted conflicting migration: {file_path}")
    
    # Update the migrations table
    update_migrations_table = input("Update django_migrations table? (y/n): ").lower() == 'y'
    if update_migrations_table:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations WHERE app = 'accounts' AND name != '0001_initial';")
            print("Removed conflicting migration records from the database.")
    
    print("\nAccounts migrations cleanup complete. Now run the following commands:")
    print("python manage.py makemigrations accounts")
    print("python manage.py migrate accounts --fake")
    print(f"\nMigrations were backed up to: {backup_dir}")

if __name__ == "__main__":
    print("This script will clean up conflicting migrations in the accounts app.")
    print("WARNING: Make sure your database is backed up before proceeding.")
    
    proceed = input("Do you want to proceed? (y/n): ").lower() == 'y'
    if proceed:
        clean_accounts_migrations()
    else:
        print("Operation cancelled.")
