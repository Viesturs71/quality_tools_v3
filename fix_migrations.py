"""
Script to fix migration issues when tables already exist in the database.
This script will mark initial migrations as applied without trying to create tables.
"""
import os
import subprocess
import sys
import django
from django.db import connection
from django.conf import settings
from django.apps import apps

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def check_table_exists(table_name):
    """Check if a table exists in the database."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = %s
            );
        """, [table_name])
        return cursor.fetchone()[0]

def get_migration_status():
    """Get the status of all migrations in the project."""
    # Run the showmigrations command and capture its output
    result = subprocess.run(
        [sys.executable, 'manage.py', 'showmigrations'],
        capture_output=True,
        text=True
    )
    
    # Parse the output to determine which migrations need to be faked
    migrations_status = {}
    current_app = None
    
    for line in result.stdout.splitlines():
        line = line.strip()
        if not line:
            continue
            
        if not line.startswith('['):
            # This is an app name
            current_app = line
            migrations_status[current_app] = {'applied': [], 'unapplied': []}
        else:
            # This is a migration
            migration_name = line[4:].strip() if line.startswith('[ ]') else line[4:].strip()
            status = 'applied' if line.startswith('[X]') else 'unapplied'
            migrations_status[current_app][status].append(migration_name)
    
    return migrations_status

def fake_all_migrations():
    """
    Fake all initial migrations for all apps without checking table existence.
    This is a more aggressive approach to fix migration issues.
    """
    print("Faking all initial migrations...")
    
    # Fake all migrations in django apps first
    core_apps = ['contenttypes', 'auth', 'admin', 'sessions']
    for app in core_apps:
        print(f"Faking initial migration for {app}...")
        try:
            subprocess.run(
                [sys.executable, 'manage.py', 'migrate', app, '0001_initial', '--fake'],
                check=True
            )
        except subprocess.CalledProcessError:
            print(f"Failed to fake initial migration for {app}, but continuing...")
    
    # Get all installed apps
    installed_apps = [app_config.label for app_config in apps.get_app_configs() 
                      if app_config.label not in core_apps]
    
    # Fake initial migrations for all project apps
    for app in installed_apps:
        print(f"Faking initial migration for {app}...")
        try:
            subprocess.run(
                [sys.executable, 'manage.py', 'migrate', app, '0001_initial', '--fake'],
                check=False  # Don't fail if an app doesn't have a migration called 0001_initial
            )
        except subprocess.CalledProcessError:
            print(f"Failed to fake initial migration for {app}, but continuing...")
    
    # Now fake apply all migrations
    print("\nFaking all migrations...")
    try:
        subprocess.run(
            [sys.executable, 'manage.py', 'migrate', '--fake'],
            check=True
        )
    except subprocess.CalledProcessError:
        print("Error during --fake migration, trying with --fake-initial instead...")
        subprocess.run(
            [sys.executable, 'manage.py', 'migrate', '--fake-initial'],
            check=False
        )

def fix_database_manually():
    """
    Fix database tables that are causing issues directly using SQL.
    This is a last resort approach when migrations fail.
    """
    print("Attempting direct database fixes...")
    
    with connection.cursor() as cursor:
        # Check if django_migrations table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'django_migrations'
            );
        """)
        if not cursor.fetchone()[0]:
            # Create django_migrations table
            print("Creating django_migrations table...")
            cursor.execute("""
                CREATE TABLE django_migrations (
                    id serial PRIMARY KEY,
                    app VARCHAR(255) NOT NULL,
                    name VARCHAR(255) NOT NULL,
                    applied TIMESTAMP WITH TIME ZONE NOT NULL
                );
            """)
    
    print("Direct database fixes applied.")
    
def fix_migrations():
    """Apply migrations with fake flag for initial migrations of existing tables."""
    print("Starting migration fix process...")
    
    # Get all installed apps
    installed_apps = [app_config.label for app_config in apps.get_app_configs()]
    
    # Check if core Django tables already exist
    core_tables_exist = all([
        check_table_exists('django_content_type'),
        check_table_exists('auth_user'),
        check_table_exists('django_migrations')
    ])
    
    if core_tables_exist:
        print("Core Django tables already exist in the database.")
        
        # Try the regular approach first
        try:
            # Fake the initial migrations for built-in apps
            for app in ['contenttypes', 'auth', 'admin', 'sessions']:
                if app in installed_apps:
                    print(f"Faking initial migration for {app}...")
                    subprocess.run(
                        [sys.executable, 'manage.py', 'migrate', app, '0001_initial', '--fake'],
                        check=True
                    )
            
            # Get migration status for all apps
            migration_status = get_migration_status()
            
            # For each app with unapplied migrations, check if tables exist
            for app, status in migration_status.items():
                if status['unapplied'] and '0001_initial' in status['unapplied']:
                    # Check if the main table for this app exists
                    try:
                        app_model_tables = [
                            model._meta.db_table
                            for model in apps.get_app_config(app.lower()).get_models()
                        ]
                        
                        if app_model_tables and check_table_exists(app_model_tables[0]):
                            print(f"Tables for {app} already exist. Faking initial migration...")
                            subprocess.run(
                                [sys.executable, 'manage.py', 'migrate', app.lower(), '0001_initial', '--fake'],
                                check=True
                            )
                    except (LookupError, AttributeError):
                        print(f"Couldn't check tables for {app}, skipping...")
            
            # Apply remaining migrations
            print("\nApplying remaining migrations...")
            subprocess.run([sys.executable, 'manage.py', 'migrate', '--fake-initial'], check=True)
            
        except subprocess.CalledProcessError:
            print("\nRegular approach failed. Trying more aggressive approach...")
            fake_all_migrations()
    else:
        print("Core Django tables don't exist or aren't accessible.")
        try:
            # Try direct database fixes
            fix_database_manually()
            
            # Then try to fake all migrations
            fake_all_migrations()
        except Exception as e:
            print(f"Error during database fix: {e}")
            print("Please consider recreating the database and starting fresh.")
    
    print("\nMigration fix process completed.")
    print("If you still encounter issues, you may need to manually fix specific migrations or recreate the database.")

if __name__ == "__main__":
    print("This script will fix migration issues by faking initial migrations for tables that already exist.")
    print("WARNING: Make sure your database structure matches your models before proceeding.")
    print("This operation may affect your database. It's recommended to backup your database first.")
    
    proceed = input("Do you want to proceed? (y/n): ").lower() == 'y'
    if proceed:
        aggressive = input("Use aggressive approach (fake all migrations without checks)? (y/n): ").lower() == 'y'
        if aggressive:
            fake_all_migrations()
        else:
            fix_migrations()
    else:
        print("Operation cancelled.")

