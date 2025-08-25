#!/usr/bin/env python
"""
Project setup script for Management System Tools
Run this script to initialize the project with proper environment variables.
"""

import os
import sys
from pathlib import Path
from django.core.management.utils import get_random_secret_key

def create_env_file():
    """Create .env file with required environment variables"""
    env_path = Path('.env')
    
    if env_path.exists():
        print("✓ .env file already exists")
        return
    
    secret_key = get_random_secret_key()
    
    env_content = f"""# Development environment variables for Management System Tools
DJANGO_SECRET_KEY={secret_key}
DEBUG=True
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# Email Configuration (optional)
# EMAIL_HOST=smtp.gmail.com
# EMAIL_PORT=587
# EMAIL_USE_TLS=True
# EMAIL_HOST_USER=your-email@gmail.com
# EMAIL_HOST_PASSWORD=your-app-password
"""
    
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✓ Created .env file with development settings")

def create_directories():
    """Create necessary directories"""
    directories = [
        'static/css',
        'static/js', 
        'static/img',
        'media',
        'locale',
        'templates/shared',
        'staticfiles'
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✓ Created project directories")

def main():
    print("Setting up Management System Tools project...")
    print("=" * 50)
    
    # Change to project directory
    project_dir = Path(__file__).parent
    os.chdir(project_dir)
    
    # Create environment file
    create_env_file()
    
    # Create directories
    create_directories()
    
    print("\n" + "=" * 50)
    print("✓ Project setup completed!")
    print("\nNext steps:")
    print("1. Run: python manage.py migrate")
    print("2. Run: python manage.py createsuperuser")
    print("3. Run: python manage.py runserver")
    print("\nFor production deployment:")
    print("1. Set DJANGO_SECRET_KEY environment variable")
    print("2. Set DEBUG=False")
    print("3. Configure proper database URL")
    print("4. Set ALLOWED_HOSTS to your domain")

if __name__ == '__main__':
    main()
