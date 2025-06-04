"""
Script to fix content type table structure issues.
This script specifically addresses the 'column django_content_type.name does not exist' error.
"""
import os
import sys
import django
from django.db import connection, transaction
from django.conf import settings

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def check_content_type_table():
    """
    Check if django_content_type table exists and has the correct structure.
    Returns a tuple (exists, has_correct_structure).
    """
    with connection.cursor() as cursor:
        # Check if table exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables 
                WHERE table_name = 'django_content_type'
            );
        """)
        table_exists = cursor.fetchone()[0]
        
        if not table_exists:
            return False, False
        
        # Check if table has the correct structure
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'django_content_type';
        """)
        columns = [row[0] for row in cursor.fetchall()]
        
        required_columns = ['id', 'app_label', 'model']
        has_name_column = 'name' in columns
        has_required_columns = all(col in columns for col in required_columns)
        
        return True, has_required_columns

def fix_content_type_table():
    """
    Fix the django_content_type table structure.
    """
    print("Checking django_content_type table structure...")
    table_exists, has_correct_structure = check_content_type_table()
    
    if not table_exists:
        print("django_content_type table doesn't exist. Creating it...")
        with connection.cursor() as cursor:
            cursor.execute("""
                CREATE TABLE django_content_type (
                    id SERIAL PRIMARY KEY,
                    app_label VARCHAR(100) NOT NULL,
                    model VARCHAR(100) NOT NULL,
                    CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model)
                );
            """)
        print("django_content_type table created successfully.")
        return True
    
    with connection.cursor() as cursor:
        # Check if 'name' column exists
        cursor.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.columns 
                WHERE table_name = 'django_content_type' AND column_name = 'name'
            );
        """)
        name_column_exists = cursor.fetchone()[0]
        
        if name_column_exists:
            print("The 'name' column exists in django_content_type table but shouldn't be there.")
            print("This is likely causing the migration error.")
            
            # Backup the table before making changes
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS django_content_type_backup AS 
                SELECT * FROM django_content_type;
            """)
            print("Created backup of django_content_type table.")
            
            # Check if we can just drop the name column
            try:
                with transaction.atomic():
                    cursor.execute("""
                        ALTER TABLE django_content_type DROP COLUMN name;
                    """)
                print("Successfully dropped 'name' column from django_content_type table.")
                return True
            except Exception as e:
                print(f"Could not drop 'name' column: {e}")
                print("Will try rebuilding the table...")
        
        # If we get here, we need to rebuild the table
        try:
            with transaction.atomic():
                # Rename the old table
                cursor.execute("""
                    ALTER TABLE django_content_type RENAME TO django_content_type_old;
                """)
                
                # Create a new table with the correct structure
                cursor.execute("""
                    CREATE TABLE django_content_type (
                        id SERIAL PRIMARY KEY,
                        app_label VARCHAR(100) NOT NULL,
                        model VARCHAR(100) NOT NULL,
                        CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model)
                    );
                """)
                
                # Copy data from old table to new table
                cursor.execute("""
                    INSERT INTO django_content_type (id, app_label, model)
                    SELECT id, app_label, model FROM django_content_type_old;
                """)
                
                # Reset the sequence
                cursor.execute("""
                    SELECT setval('django_content_type_id_seq', 
                                 (SELECT MAX(id) FROM django_content_type), true);
                """)
                
                print("Successfully rebuilt django_content_type table with correct structure.")
                return True
                
        except Exception as e:
            print(f"Error rebuilding django_content_type table: {e}")
            print("Attempting recovery...")
            
            try:
                # If the previous operations failed, try to restore the original table
                cursor.execute("""
                    DROP TABLE IF EXISTS django_content_type;
                """)
                cursor.execute("""
                    ALTER TABLE django_content_type_old RENAME TO django_content_type;
                """)
                print("Restored original table after error.")
            except Exception as recovery_error:
                print(f"Recovery failed: {recovery_error}")
                print("Database may be in an inconsistent state. Manual intervention required.")
            
            return False

def recreate_content_types():
    """
    Recreate content types for all installed apps.
    """
    print("Recreating content types...")
    try:
        from django.contrib.contenttypes.management import create_contenttypes
        from django.apps import apps
        
        # Clear existing content types
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE django_content_type RESTART IDENTITY CASCADE;")
        
        # Recreate content types for all apps
        for app_config in apps.get_app_configs():
            create_contenttypes(app_config)
        
        print("Content types recreated successfully.")
        return True
    except Exception as e:
        print(f"Error recreating content types: {e}")
        return False

def main():
    """
    Main function to fix content type issues.
    """
    print("Starting content type table fix process...")
    
    # Fix the table structure
    if fix_content_type_table():
        print("Content type table structure fixed.")
        
        # Optionally recreate content types
        recreate = input("Do you want to recreate all content types? (y/n): ").lower() == 'y'
        if recreate:
            if recreate_content_types():
                print("Content types have been recreated.")
            else:
                print("Failed to recreate content types.")
    else:
        print("Failed to fix content type table structure.")
    
    print("\nNext steps:")
    print("1. Run migrations with --fake-initial flag:")
    print("   python manage.py migrate --fake-initial")
    print("2. If issues persist, try using the fix_migrations.py script again with the aggressive approach.")

if __name__ == "__main__":
    print("This script will fix issues with the django_content_type table structure.")
    print("WARNING: This operation will modify your database. It's recommended to backup your database first.")
    
    proceed = input("Do you want to proceed? (y/n): ").lower() == 'y'
    if proceed:
        main()
    else:
        print("Operation cancelled.")
