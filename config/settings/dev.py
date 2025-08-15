"""
Development settings for Quality Tools project.
"""

from .base import *
import dj_database_url
from decouple import config

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-development-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database - use environment variable or fallback to SQLite
DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL', default='sqlite:///db.sqlite3'),
        conn_max_age=600
    )
}

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration for development
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'verbose',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'INFO',
            'formatter': 'verbose',
            'filename': BASE_DIR / 'logs/django-dev.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': True,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    }
}

# Debug toolbar settings
try:
    import debug_toolbar
    INSTALLED_APPS += ['debug_toolbar']
    MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']
    INTERNAL_IPS = ['127.0.0.1']
    DEBUG_TOOLBAR_CONFIG = {
        'INTERCEPT_REDIRECTS': False,
    }
except ImportError:
    pass
