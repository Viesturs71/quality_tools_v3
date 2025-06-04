"""
Script to reset equipment migrations.
This script will:
1. Delete all migration files from the equipment app
2. Delete the equipment app entry from the django_migrations table
3. Create a new initial migration

Usage:
python reset_equipment_migrations.py
"""
import os
import sys
import subprocess
import psycopg
from django.conf import settings

# Add project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

# Get database settings from Django settings
try:
    from django.conf import settings
    DB_NAME = settings.DATABASES['default']['NAME']
    DB_USER = settings.DATABASES['default']['USER']
    DB_PASSWORD = settings.DATABASES['default'].get('PASSWORD', '')
    DB_HOST = settings.DATABASES['default'].get('HOST', 'localhost')
    DB_PORT = settings.DATABASES['default'].get('PORT', '5432')
except (ImportError, KeyError) as e:
    print(f"Error loading database settings: {e}")
    print("Please make sure Django settings are correctly configured.")
    sys.exit(1)

def run_command(command):
    """Run a shell command and return the output."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(command, shell=True, check=True, 
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               text=True)
        print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Command failed with error: {e}")
        print(f"Error output: {e.stderr}")
        return False

def remove_migration_files():
    """Remove all migration files from the equipment app."""
    migrations_dir = os.path.join('equipment', 'migrations')
    if not os.path.exists(migrations_dir):
        print(f"Migrations directory {migrations_dir} does not exist.")
        return
    
    for filename in os.listdir(migrations_dir):
        if filename.endswith('.py') and filename != '__init__.py':
            file_path = os.path.join(migrations_dir, filename)
            try:
                os.remove(file_path)
                print(f"Removed migration file: {file_path}")
            except Exception as e:
                print(f"Error removing {file_path}: {e}")

def clean_database():
    """Remove equipment app from django_migrations table and drop relevant tables."""
    connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    try:
        # Connect to the database
        with psycopg.connect(connection_string) as conn:
            with conn.cursor() as cur:
                # Delete equipment migrations from django_migrations
                cur.execute("DELETE FROM django_migrations WHERE app = 'equipment'")
                print(f"Deleted {cur.rowcount} rows from django_migrations for app 'equipment'")
                
                # Attempt to drop tables that might cause conflicts
                # Note: Some tables might not exist, so we'll catch and ignore errors
                tables_to_drop = [
                    "equipment_equipmentregistry",
                    "equipment_equipment",
                    "equipment_equipmentdocument",
                    "equipment_maintenancerecord",
                    "equipment_equipmenttype",
                    "equipment_department"
                ]
                
                for table in tables_to_drop:
                    try:
                        cur.execute(f'DROP TABLE IF EXISTS "{table}" CASCADE')
                        print(f"Dropped table {table}")
                    except Exception as e:
                        print(f"Error dropping table {table}: {e}")
                
            conn.commit()
            print("Database cleaned successfully")
            
    except Exception as e:
        print(f"Database error: {e}")
        return False
    
    return True

def create_migrations_and_migrate():
    """Create new migrations and apply them."""
    # Create __init__.py if it doesn't exist
    migrations_dir = os.path.join('equipment', 'migrations')
    os.makedirs(migrations_dir, exist_ok=True)
    
    init_file = os.path.join(migrations_dir, '__init__.py')
    if not os.path.exists(init_file):
        with open(init_file, 'w') as f:
            f.write("# This file is required for Python to recognize this directory as a package.\n")
        print(f"Created {init_file}")
    
    # Make migrations
    if not run_command('python manage.py makemigrations equipment'):
        return False
    
    # Migrate
    return run_command('python manage.py migrate equipment')

if __name__ == "__main__":
    print("Starting equipment migrations reset...")
    
    # Step 1: Remove existing migration files
    remove_migration_files()
    
    # Step 2: Clean database
    if clean_database():
        # Step 3: Create new migrations and migrate
        if create_migrations_and_migrate():
            print("Equipment migrations reset successfully!")
        else:
            print("Failed to create or apply migrations.")
    else:
        print("Failed to clean database.")
