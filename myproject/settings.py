import os
from pathlib import Path

import dj_database_url
from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "jūsu_drošais_noslēpums")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1", "http://localhost"]

# ---------------------------------------------------------------------------
# Django applications
# ---------------------------------------------------------------------------
INSTALLED_APPS = [
    # Django core
    'django_extensions',
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Third‑party apps
    "crispy_forms",
    "crispy_bootstrap4",
    "mptt",
    "rosetta",
    "simple_history",

    # Local apps
    "accounts.apps.AccountsConfig",   # Use the app config to ensure unique labels
    "equipment",
    "quality_docs",
    "personnel",
    "dashboard",
    "company",  # Keep this and remove any 'companies' reference
    "standards",
    "core",
]

# ---------------------------------------------------------------------------
# Crispy Forms
# ---------------------------------------------------------------------------
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap4"

# ---------------------------------------------------------------------------
# Middleware
# ---------------------------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.locale.LocaleMiddleware",  # Make sure this middleware is present
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "myproject.urls"

# ---------------------------------------------------------------------------
# Templates
# ---------------------------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "myproject.context_processors.user_modules",
                "myproject.context_processors.institution_settings",
                "quality_docs.context_processors.document_counts",
                "core.context_processors.admin_navigation", 
            ],
        },
    },
]

WSGI_APPLICATION = "myproject.wsgi.application"

# ---------------------------------------------------------------------------
# Database (Heroku‑style url, defaulting to local Postgres)
# ---------------------------------------------------------------------------
DATABASES = {
    "default": dj_database_url.config(
        default=os.getenv(
            "DATABASE_URL",
            "postgres://postgres:Emilija2004@localhost:5432/quality_tools_3",
        ),
        conn_max_age=600,
        ssl_require=False,
    )
}

# ---------------------------------------------------------------------------
# Custom user model
# ---------------------------------------------------------------------------
AUTH_USER_MODEL = "accounts.CustomUser"

# ---------------------------------------------------------------------------
# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/
# ---------------------------------------------------------------------------
LANGUAGE_CODE = "en"

LANGUAGES = [
    ("en", _("English")),
    ("lv", _("Latviešu")),
    ("de", _("Deutsch")),
    ("es", _("Español")),
]

TIME_ZONE = "Europe/Riga"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Use the standard locale directory location for consistency
LOCALE_PATHS = [
    os.path.join(BASE_DIR, "locale"),
]

# ---------------------------------------------------------------------------
# Static & media files
# ---------------------------------------------------------------------------
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ---------------------------------------------------------------------------
# Default Django settings
# ---------------------------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
LOGIN_REDIRECT_URL = '/dashboard/'
LOGIN_URL = "/login/"
LOGOUT_REDIRECT_URL = "/accounts/login/"

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
]

# ---------------------------------------------------------------------------
# Django REST Framework + Spectacular / Swagger
# ---------------------------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.SessionAuthentication",
        "rest_framework.authentication.BasicAuthentication",
    ],
}

SWAGGER_SETTINGS = {
    "SECURITY_DEFINITIONS": {
        "Basic": {"type": "basic"},
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
        },
    }
}

SPECTACULAR_SETTINGS = {
    "TITLE": "Kvalitātes Dokumentu API",
    "DESCRIPTION": "API dokumentācija kvalitātes dokumentu pārvaldībai.",
    "VERSION": "1.0.0",
    "SERVE_INCLUDE_SCHEMA": False,
    "SWAGGER_UI_SETTINGS": {
        "deepLinking": True,
        "defaultModelRendering": "model",
        "displayRequestDuration": True,
    },
}

# ---------------------------------------------------------------------------
# File encodings
# ---------------------------------------------------------------------------
FILE_CHARSET = "utf-8"
DEFAULT_CHARSET = "utf-8"

# ---------------------------------------------------------------------------
# Rosetta
# ---------------------------------------------------------------------------
ROSETTA_MESSAGES_SOURCE_LANGUAGE = "en"
ROSETTA_MESSAGES_PER_PAGE = 25
ROSETTA_ENABLE_TRANSLATION_SUGGESTIONS = True
ROSETTA_REQUIRES_SUPERUSER = False
def ROSETTA_ACCESS_CONTROL_FUNCTION(user):
    return True
ROSETTA_SHOW_AT_ADMIN_PANEL = True
ROSETTA_UWSGI_AUTO_RELOAD = True  # Auto reload uwsgi when translations change

# ---------------------------------------------------------------------------
# Cache settings
# ---------------------------------------------------------------------------
if DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.dummy.DummyCache',
        }
    }
else:
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        }
    }
