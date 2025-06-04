"""
Script to fix inconsistent migration history.
Specifically addresses the error:
"Migration auth.0001_initial is applied before its dependency contenttypes.0001_initial"
"""
import os
import sys
import django
from django.db import connection, transaction
from django.conf import settings
from django.apps import apps

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def check_migration_tables():
    """Check if django_migrations table exists and has records."""
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'django_migrations'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            return False, 0
        
        # Count migrations
        cursor.execute("SELECT COUNT(*) FROM django_migrations;")
        count = cursor.fetchone()[0]
        
        return True, count

def backup_migrations_table():
    """Create a backup of the migrations table."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS django_migrations_backup AS 
                SELECT * FROM django_migrations;
            """)
        print("Created backup of django_migrations table.")
        return True
    except Exception as e:
        print(f"Failed to backup migrations table: {e}")
        return False

def clear_migrations():
    """Clear all migration records from the database."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM django_migrations;")
        print("Cleared all migration records.")
        return True
    except Exception as e:
        print(f"Failed to clear migrations: {e}")
        return False

def add_migration(app, name, applied_datetime=None):
    """Add a specific migration record to the database."""
    if applied_datetime is None:
        # Use current timestamp if not provided
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES (%s, %s, NOW());
            """, [app, name])
    else:
        with connection.cursor() as cursor:
            cursor.execute("""
                INSERT INTO django_migrations (app, name, applied) 
                VALUES (%s, %s, %s);
            """, [app, name, applied_datetime])
    
    print(f"Added migration record for {app}.{name}")

def get_app_migrations():
    """Get all migrations from the backup table."""
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT app, name, applied FROM django_migrations_backup
            ORDER BY id;
        """)
        return cursor.fetchall()

def restore_migrations_in_correct_order():
    """Restore migrations in the correct dependency order."""
    # Get all migrations from backup
    migrations = get_app_migrations()
    
    # Dictionary to store migrations by app
    app_migrations = {}
    for app, name, applied in migrations:
        if app not in app_migrations:
            app_migrations[app] = []
        app_migrations[app].append((name, applied))
    
    # Order in which apps should be migrated (critical ones first)
    core_apps_order = [
        'contenttypes',  # Must be first
        'auth',          # Depends on contenttypes
        'admin',         # Depends on auth
        'sessions',      # Standard Django app
        # All other apps can follow
    ]
    
    # Add all core migrations first in the correct order
    with transaction.atomic():
        # First, handle core apps in the correct order
        for app in core_apps_order:
            if app in app_migrations:
                for name, applied in sorted(app_migrations[app], key=lambda x: x[0]):
                    add_migration(app, name, applied)
                # Remove from dict to avoid duplicates
                del app_migrations[app]
        
        # Then add all remaining migrations
        for app, migrations_list in app_migrations.items():
            for name, applied in sorted(migrations_list, key=lambda x: x[0]):
                add_migration(app, name, applied)
    
    print("Restored migrations in correct dependency order.")

def manually_fix_migrations():
    """Manually add critical migrations in the correct order."""
    # Timestamp for consistent ordering
    from django.utils import timezone
    now = timezone.now()
    
    with transaction.atomic():
        # Add essential migrations in correct order
        add_migration('contenttypes', '0001_initial', now)
        add_migration('auth', '0001_initial', now)
        add_migration('admin', '0001_initial', now)
        add_migration('admin', '0002_logentry_remove_auto_add', now)
        add_migration('admin', '0003_logentry_add_action_flag_choices', now)
        add_migration('sessions', '0001_initial', now)
        
        # Then fake other app migrations
        for app_config in apps.get_app_configs():
            if app_config.label not in ['contenttypes', 'auth', 'admin', 'sessions']:
                # Add a fake initial migration if this is a custom app with models
                if app_config.models and hasattr(app_config, 'migrations_module'):
                    add_migration(app_config.label, '0001_initial', now)
    
    print("Manually added critical migrations in correct order.")

def main():
    """Main function to run the fix."""
    print("Starting migration history fix process...")
    
    # Check migration table
    table_exists, count = check_migration_tables()
    if not table_exists:
        print("django_migrations table doesn't exist. You need to run migrations first.")
        return False
    
    print(f"Found {count} migration records in the database.")
    
    # Backup migrations table
    if not backup_migrations_table():
        print("Could not backup migrations table. Aborting.")
        return False
    
    # Choose fixing strategy
    strategy = input("Choose fixing strategy:\n"
                    "1. Restore from backup in correct order (recommended if backup succeeded)\n"
                    "2. Manually add critical migrations only\n"
                    "Enter 1 or 2: ")
    
    # Clear existing migrations
    if not clear_migrations():
        print("Could not clear migrations table. Aborting.")
        return False
    
    # Apply chosen strategy
    if strategy == '1':
        restore_migrations_in_correct_order()
    else:
        manually_fix_migrations()
    
    print("\nMigration history has been fixed.")
    print("\nNext steps:")
    print("1. Run migrations with --fake-initial flag:")
    print("   python manage.py migrate --fake-initial")
    print("2. If issues persist, try running migrations for specific apps one by one:")
    print("   python manage.py migrate [your_app] --fake")
    
    return True

if __name__ == "__main__":
    print("This script will fix inconsistent migration history issues.")
    print("It specifically addresses the error where auth migrations were applied before contenttypes.")
    print("WARNING: This operation will modify your database. It's recommended to backup your database first.")
    
    proceed = input("Do you want to proceed? (y/n): ").lower() == 'y'
    if proceed:
        main()
    else:
        print("Operation cancelled.")
