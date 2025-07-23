"""
Base settings for Quality Tools project.
"""

from pathlib import Path
from decouple import config
from django.utils.translation import gettext_lazy as _
import dj_database_url

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Security
SECRET_KEY = config("DJANGO_SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)
ALLOWED_HOSTS = [host.strip() for host in config("ALLOWED_HOSTS").split(",")]

# Database (Heroku/Postgres)
DATABASES = {
    "default": dj_database_url.parse(config("DATABASE_URL"), conn_max_age=600)
}

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party
    'crispy_forms',
    'crispy_bootstrap5',
    'mptt',
    'rosetta',
    'simple_history',
    # Project apps
    'apps.accounts.apps.AccountsConfig',
    'apps.authentication.apps.AuthenticationConfig',
    'apps.company.apps.CompanyConfig',
    'apps.equipment.apps.EquipmentConfig',
    'apps.documents.apps.DocumentsConfig',
    'apps.personnel.apps.PersonnelConfig',
    'apps.standards.apps.StandardsConfig',
    'apps.dashboard.apps.DashboardConfig',
    'apps.users.apps.UsersConfig',
    'apps.debug_tools',
    'apps.core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',  # After SessionMiddleware
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
        'DIRS': [BASE_DIR / 'templates'],
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

# Authentication backends
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

# Internationalization
LANGUAGE_CODE = 'en'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = [
    ('en', 'English'),
    ('lv', 'Latviešu'),
]

LOCALE_PATHS = [
    BASE_DIR / 'locale',
]

LANGUAGE_COOKIE_NAME = 'django_language'
LANGUAGE_COOKIE_PATH = '/'
LANGUAGE_COOKIE_HTTPONLY = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Login/Logout URLs
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'

# Session configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.db'
SESSION_COOKIE_NAME = 'sessionid'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}

# Rosetta settings
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_MESSAGES_PER_PAGE = 25
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_POFILE_WRAP_WIDTH = 80

# Admin settings
ADMIN_URL = 'admin/'

# Navigation apps configuration
NAVIGATION_APPS = {
    'users': {
        'icon': 'fa-users',
        'models': ['CustomUser', 'UserProfile'],
        'permissions': ['view_user', 'add_user']
    },
    'documents': {
        'icon': 'fa-file-text',
        'models': ['Document', 'DocumentSection'],
        'permissions': ['view_document']
    },
    'equipment': {
        'icon': 'fa-tools',
        'models': ['Equipment', 'EquipmentCategory'],
        'permissions': ['view_equipment']
    },
    'personnel': {
        'icon': 'fa-id-card',
        'models': ['Employee', 'Qualification'],
        'permissions': ['view_employee']
    },
    'standards': {
        'icon': 'fa-book',
        'models': ['Standard', 'StandardSection'],
        'permissions': ['view_standard']
    },
}
