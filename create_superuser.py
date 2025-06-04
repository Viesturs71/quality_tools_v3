"""
Script to create a Django superuser programmatically.
"""
import os
import django
import getpass
from django.contrib.auth import get_user_model

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')
django.setup()

def create_superuser():
    """Create a Django superuser."""
    User = get_user_model()
    
    # Prompt for username, email, and password with proper input prompts
    print("Creating a new superuser:")
    username = input("Username: ").strip()
    email = input("Email: ").strip()
    password = getpass.getpass("Password: ")
    password_confirm = getpass.getpass("Confirm password: ")
    
    # Validate input
    if not username:
        print("Error: Username cannot be empty.")
        return
    
    if not email:
        print("Error: Email cannot be empty.")
        return
    
    if password != password_confirm:
        print("Error: Passwords do not match.")
        return
    
    if not password:
        print("Error: Password cannot be empty.")
        return
    
    # Create the superuser
    if not User.objects.filter(username=username).exists():
        try:
            User.objects.create_superuser(username=username, email=email, password=password)
            print(f"Superuser '{username}' created successfully.")
        except Exception as e:
            print(f"Error creating superuser: {e}")
    else:
        print(f"Superuser '{username}' already exists.")

if __name__ == "__main__":
    create_superuser()
