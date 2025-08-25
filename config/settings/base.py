"""
Base settings for Quality Tools project.
"""

import os
import sys
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Add apps directory to Python path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))

# Load environment variables from .env file
def load_env_file():
    env_file = BASE_DIR / '.env'
    if env_file.exists():
        with open(env_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    os.environ.setdefault(key.strip(), value.strip())

load_env_file()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
if not SECRET_KEY:
    if os.environ.get('DEBUG', 'False').lower() == 'true':
        # Generate a temporary secret key for development
        SECRET_KEY = get_random_secret_key()
        print("Warning: Using auto-generated SECRET_KEY. Set DJANGO_SECRET_KEY in .env file.")
    else:
        raise ValueError("DJANGO_SECRET_KEY environment variable is required for production")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'rosetta',
]

LOCAL_APPS = [
    'apps.users',
    'apps.accounts',
    'apps.authentication',
    'apps.company',
    'apps.dashboard',
    'apps.documents',
    'apps.equipment',
    'apps.audits',
    'apps.methods',
    'apps.personnel',
    'apps.standards',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')

# Handle both postgres:// and postgresql:// URLs for Heroku compatibility
if DATABASE_URL.startswith('postgres://'):
    DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)

if DATABASE_URL.startswith('sqlite'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / DATABASE_URL.replace('sqlite:///', ''),
        }
    }
else:
    # For PostgreSQL and other databases
    DATABASES = {
        'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
    }

# Custom User Model
AUTH_USER_MODEL = 'users.CustomUser'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGES = [
    ('lv', 'Latvian'),
    ('en', 'English'),
]

LANGUAGE_CODE = 'en'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Navigation Apps Configuration
NAVIGATION_APPS = {
    'users': {
        'icon': 'fa-users',
        'models': ['CustomUser', 'UserProfile'],
        'permissions': ['view_user', 'add_user']
    },
    'accounts': {
        'icon': 'fa-building',
        'models': ['Account', 'Subscription'],
        'permissions': ['view_account']
    },
    'documents': {
        'icon': 'fa-file-text',
        'models': ['Document', 'DocumentSection'],
        'permissions': ['view_document']
    },
    'equipment': {
        'icon': 'fa-cogs',
        'models': ['Equipment', 'EquipmentCategory'],
        'permissions': ['view_equipment']
    },
    'audits': {
        'icon': 'fa-clipboard-check',
        'models': ['Audit', 'AuditFinding'],
        'permissions': ['view_audit']
    },
    'standards': {
        'icon': 'fa-certificate',
        'models': ['Standard', 'StandardSection'],
        'permissions': ['view_standard']
    },
    'methods': {
        'icon': 'fa-flask',
        'models': ['Method', 'MethodValidation'],
        'permissions': ['view_method']
    },
    'personnel': {
        'icon': 'fa-id-card',
        'models': ['Employee', 'Position'],
        'permissions': ['view_employee']
    },
    'company': {
        'icon': 'fa-sitemap',
        'models': ['Company', 'Department'],
        'permissions': ['view_company']
    },
}
