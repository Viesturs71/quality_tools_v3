"""
Script to fix issues with the django_content_type table structure.

This script addresses the specific error:
django.db.utils.ProgrammingError: column django_content_type.name does not exist
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
    Check if the django_content_type table exists and has the correct structure.
    Returns tuple (exists, has_name_column, schema_mismatch)
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
            return False, False, True
        
        # Check table columns
        cursor.execute("""
            SELECT column_name FROM information_schema.columns 
            WHERE table_name = 'django_content_type';
        """)
        columns = [row[0] for row in cursor.fetchall()]
        
        expected_columns = ['id', 'app_label', 'model']
        has_name_column = 'name' in columns
        
        # Check if expected columns exist
        schema_mismatch = not all(col in columns for col in expected_columns)
        
        return table_exists, has_name_column, schema_mismatch

def fix_content_type_table():
    """
    Fix the django_content_type table to match Django's expected structure.
    Specifically dealing with the 'name' column issue.
    """
    print("Checking django_content_type table structure...")
    table_exists, has_name_column, schema_mismatch = check_content_type_table()
    
    if not table_exists:
        print("django_content_type table doesn't exist. Creating it with correct structure...")
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
    
    if schema_mismatch:
        print("django_content_type table has incorrect schema.")
        print("Backing up and recreating with correct structure...")
        
        try:
            with connection.cursor() as cursor:
                # Create backup table if it doesn't exist
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS django_content_type_backup AS 
                    SELECT * FROM django_content_type;
                """)
                print("Backup created as django_content_type_backup.")
                
                # Drop and recreate table with correct schema
                with transaction.atomic():
                    # Drop the table
                    cursor.execute("DROP TABLE django_content_type;")
                    
                    # Create with correct schema
                    cursor.execute("""
                        CREATE TABLE django_content_type (
                            id SERIAL PRIMARY KEY,
                            app_label VARCHAR(100) NOT NULL,
                            model VARCHAR(100) NOT NULL,
                            CONSTRAINT django_content_type_app_label_model_key UNIQUE (app_label, model)
                        );
                    """)
                    
                    # Try to restore data
                    try:
                        cursor.execute("""
                            INSERT INTO django_content_type (id, app_label, model)
                            SELECT id, app_label, model FROM django_content_type_backup;
                        """)
                        print("Data restored from backup.")
                    except Exception as e:
                        print(f"Error restoring data: {e}")
                        print("You may need to manually recreate content types.")
            
            print("django_content_type table recreated with correct schema.")
            return True
            
        except Exception as e:
            print(f"Error fixing django_content_type table: {e}")
            return False
    
    if has_name_column:
        print("Found 'name' column in django_content_type table.")
        print("This column is not expected in newer Django versions.")
        
        try:
            with connection.cursor() as cursor:
                # Try to drop the name column
                with transaction.atomic():
                    cursor.execute("""
                        ALTER TABLE django_content_type DROP COLUMN IF EXISTS name;
                    """)
            print("Successfully removed 'name' column.")
            return True
        except Exception as e:
            print(f"Error removing 'name' column: {e}")
            return False
    
    print("django_content_type table structure appears to be correct.")
    return True

def clear_content_type_table():
    """Truncate the content type table to allow Django to rebuild it."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("TRUNCATE django_content_type RESTART IDENTITY CASCADE;")
        print("Content type table cleared. Django will rebuild content types on next run.")
        return True
    except Exception as e:
        print(f"Error clearing content type table: {e}")
        return False

def clear_migrations_record():
    """Clear migration records for contenttypes app to allow reapplying migrations."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                DELETE FROM django_migrations 
                WHERE app = 'contenttypes';
            """)
        print("Migration records for contenttypes app cleared.")
        return True
    except Exception as e:
        print(f"Error clearing migration records: {e}")
        return False

def main():
    """Main function to run the fixes."""
    print("Starting content type table fix process...")
    
    # Fix the table structure
    structure_fixed = fix_content_type_table()
    if not structure_fixed:
        print("Failed to fix table structure.")
        return False
    
    # Ask user about clearing the table
    clear_table = input("Do you want to clear the content type table to let Django rebuild it? (y/n): ").lower() == 'y'
    if clear_table:
        if not clear_content_type_table():
            print("Failed to clear content type table.")
            return False
    
    # Ask user about clearing migration records
    clear_migrations = input("Do you want to clear migration records for contenttypes app? (y/n): ").lower() == 'y'
    if clear_migrations:
        if not clear_migrations_record():
            print("Failed to clear migration records.")
            return False
    
    print("\nNext steps:")
    print("1. Run migrations with --fake-initial flag:")
    print("   python manage.py migrate --fake-initial")
    print("2. If issues persist, try running migrations for specific apps one by one:")
    print("   python manage.py migrate contenttypes --fake")
    print("   python manage.py migrate auth --fake")
    print("   python manage.py migrate admin --fake")
    print("   python manage.py migrate sessions --fake")
    print("   python manage.py migrate [your_app] --fake")
    print("3. Finally, try running regular migrations:")
    print("   python manage.py migrate")
    
    return True

if __name__ == "__main__":
    print("This script will fix issues with the django_content_type table structure.")
    print("It addresses the 'column django_content_type.name does not exist' error.")
    print("WARNING: This operation will modify your database. It's recommended to backup your database first.")
    
    proceed = input("Do you want to proceed? (y/n): ").lower() == 'y'
    if proceed:
        main()
    else:
        print("Operation cancelled.")
