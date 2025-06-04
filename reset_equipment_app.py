"""
Script to completely reset the equipment app:
1. Delete all migration files except __init__.py
2. Remove migration records from the database
3. Drop tables related to the equipment app
"""
import os
import sys
import django
from django.db import connection

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def reset_equipment_app():
    """
    Completely reset the equipment app by:
    1. Deleting migration files
    2. Removing migration records from the database
    3. Dropping related tables
    """
    app_name = 'equipment'
    project_root = os.path.dirname(os.path.abspath(__file__))
    migrations_dir = os.path.join(project_root, app_name, 'migrations')
    
    print(f"Starting complete reset of the {app_name} app...")
    
    # Step 1: Delete migration files
    if os.path.exists(migrations_dir):
        print("\nDeleting migration files...")
        all_files = os.listdir(migrations_dir)
        migration_files = [f for f in all_files 
                          if f.endswith('.py') and f != '__init__.py']
        
        for filename in migration_files:
            file_path = os.path.join(migrations_dir, filename)
            try:
                os.remove(file_path)
                print(f"Deleted: {filename}")
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
    else:
        print(f"No migrations directory found at {migrations_dir}")
    
    # Step 2: Clean database
    print("\nCleaning database...")
    with connection.cursor() as cursor:
        # Remove migration records
        try:
            cursor.execute(f"DELETE FROM django_migrations WHERE app = '{app_name}';")
            print("Removed migration records from the database.")
        except Exception as e:
            print(f"Error removing migration records: {e}")
        
        # Find and drop equipment tables
        try:
            print("Finding all equipment tables...")
            cursor.execute("""
                SELECT tablename FROM pg_tables 
                WHERE tablename LIKE 'equipment_%' AND schemaname = 'public';
            """)
            tables = cursor.fetchall()
            
            # First drop the problematic table that's causing issues
            try:
                cursor.execute("DROP TABLE IF EXISTS equipment_equipmentregistry CASCADE;")
                print("Dropped equipment_equipmentregistry table if it existed.")
            except Exception as e:
                print(f"Error dropping equipment_equipmentregistry: {e}")
            
            # Drop all remaining equipment tables
            for table in tables:
                table_name = table[0]
                try:
                    cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
                    print(f"Dropped table: {table_name}")
                except Exception as e:
                    print(f"Error dropping {table_name}: {e}")
            
            # Drop sequences related to equipment tables
            cursor.execute("""
                SELECT sequence_name FROM information_schema.sequences
                WHERE sequence_name LIKE 'equipment_%';
            """)
            sequences = cursor.fetchall()
            for seq in sequences:
                seq_name = seq[0]
                try:
                    cursor.execute(f"DROP SEQUENCE IF EXISTS {seq_name} CASCADE;")
                    print(f"Dropped sequence: {seq_name}")
                except Exception as e:
                    print(f"Error dropping sequence {seq_name}: {e}")
            
            # Drop indexes related to equipment tables
            cursor.execute("""
                SELECT indexname FROM pg_indexes 
                WHERE indexname LIKE 'equipment_%' OR indexname LIKE 'dept_%';
            """)
            indexes = cursor.fetchall()
            for idx in indexes:
                idx_name = idx[0]
                try:
                    cursor.execute(f"DROP INDEX IF EXISTS {idx_name} CASCADE;")
                    print(f"Dropped index: {idx_name}")
                except Exception as e:
                    print(f"Could not drop index {idx_name}: {e}")
        except Exception as e:
            print(f"Error finding or dropping tables: {e}")
    
    print("\nReset completed successfully!")
    print("Next steps:")
    print("1. Run: python manage.py makemigrations equipment")
    print("2. Run: python manage.py migrate equipment")
    print("3. Create any necessary initial data")

if __name__ == "__main__":
    reset_equipment_app()
