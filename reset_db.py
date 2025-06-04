"""
Script to reset the database and clean migrations.
This will completely reset the database and delete all migrations.
"""
import os
import sys
import django
from django.db import connection

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def reset_database():
    """Reset the database and clean migrations."""
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Step 1: Find all apps with migrations
    apps = [d for d in os.listdir(project_root) 
            if os.path.isdir(os.path.join(project_root, d))
            and os.path.exists(os.path.join(project_root, d, 'migrations'))
            and not d.startswith('.') and not d == '__pycache__']
    
    print(f"Found apps with migrations: {', '.join(apps)}")
    
    # Step 2: Clean migrations from database
    with connection.cursor() as cursor:
        print("\nRemoving migration records from database...")
        cursor.execute("DELETE FROM django_migrations;")
        print("Migration records removed from database.")
        
        # Step 3: Drop app tables with potential conflicts
        print("\nDropping application tables...")
        for app in apps:
            try:
                # Get all tables for this app
                cursor.execute(f"""
                    SELECT tablename FROM pg_tables 
                    WHERE tablename LIKE '{app}_%' AND schemaname = 'public';
                """)
                tables = cursor.fetchall()
                
                for table in tables:
                    table_name = table[0]
                    try:
                        cursor.execute(f"DROP TABLE IF EXISTS {table_name} CASCADE;")
                        print(f"Dropped table: {table_name}")
                    except Exception as e:
                        print(f"Error dropping {table_name}: {e}")
                
                # Get and drop sequences
                cursor.execute(f"""
                    SELECT sequence_name FROM information_schema.sequences
                    WHERE sequence_name LIKE '{app}_%';
                """)
                sequences = cursor.fetchall()
                for seq in sequences:
                    seq_name = seq[0]
                    try:
                        cursor.execute(f"DROP SEQUENCE IF EXISTS {seq_name} CASCADE;")
                        print(f"Dropped sequence: {seq_name}")
                    except Exception as e:
                        print(f"Error dropping sequence {seq_name}: {e}")
                
                # Get and drop indexes
                cursor.execute(f"""
                    SELECT indexname FROM pg_indexes 
                    WHERE indexname LIKE '{app}_%' OR indexname LIKE 'dept_%';
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
                print(f"Error processing app {app}: {e}")
    
    # Step 4: Delete migration files
    total_removed = 0
    for app in apps:
        migrations_dir = os.path.join(project_root, app, 'migrations')
        
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
    
    print(f"\nDatabase reset and migration cleanup complete. Removed {total_removed} migration files.")
    print("Next steps:")
    print("1. Run: python manage.py makemigrations")
    print("2. Run: python manage.py migrate")

if __name__ == "__main__":
    response = input("This will delete ALL migrations and reset the database. Are you sure? (y/N): ")
    if response.lower() == 'y':
        reset_database()
    else:
        print("Operation cancelled.")
