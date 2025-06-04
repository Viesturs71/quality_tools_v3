import os
import django
from django.db import connection

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def drop_contenttypes():
    """Drop the django_content_type table if it exists."""
    with connection.cursor() as cursor:
        cursor.execute("""
            DROP TABLE IF EXISTS django_content_type CASCADE;
        """)
        print("Dropped table: django_content_type")

if __name__ == "__main__":
    print("Removing conflicting contenttypes table...")
    drop_contenttypes()
    print("Now run: python manage.py migrate --fake-initial")
