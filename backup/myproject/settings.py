## 🛠️ **`settings.py`**
import os
from pathlib import Path

from django.utils.translation import gettext_lazy as _

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "jūsu_drošais_noslēpums")
DEBUG = os.getenv("DJANGO_DEBUG", "True") == "True"
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

CSRF_TRUSTED_ORIGINS = ["http://127.0.0.1", "http://localhost"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rosetta",
    "accounts",
    "equipment.apps.EquipmentConfig",
    "crispy_forms",
    "crispy_bootstrap5",
    "mptt",  # Obligāti MPTT modeļiem
    "django_mptt_admin",  # ✅ Šis ir nepieciešams!
    "simple_history",
    "import_export",
    'personnel.apps.PersonnelConfig',
    "company.apps.CompanyConfig",
    # "methods.apps.MethodsConfig",
    "quality_docs.apps.QualityDocsConfig",
    'drf_spectacular',
    'drf_spectacular_sidecar',
    "rest_framework",
    "drf_yasg",
    "django_extensions",
    'audits',
]

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

MIDDLEWARE = [
    "django.middleware.locale.LocaleMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "simple_history.middleware.HistoryRequestMiddleware",
]

ROOT_URLCONF = "myproject.urls"

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),  # Add the central templates directory
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "myproject.context_processors.user_modules",
                "django.template.context_processors.i18n",
                'myproject.context_processors.navigation',  # Pievienojam jauno
            ],
        },
    },
]

WSGI_APPLICATION = "myproject.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "quality_tools_2_1",  # Datubāzes nosaukums
        "USER": "postgres",  # PostgreSQL lietotājs
        "PASSWORD": "Emilija2004",  # PostgreSQL parole
        "HOST": "localhost",
        "PORT": "5432",
    }
}

AUTH_USER_MODEL = "accounts.CustomUser"

LANGUAGE_CODE = "en"
LANGUAGES = [
    ('en', _('English')),
    ('lv', _('Latviešu')),
    ('de', _('Deutsch')),
    ('es', _('Español')),
]
TIME_ZONE = "Europe/Riga"
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = [
    BASE_DIR / "locale",
]

STATIC_URL = "/static/"
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")  # Nodrošina statisko failu savākšanu

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/login/"
LOGIN_REDIRECT_URL = 'home'
LOGOUT_REDIRECT_URL = "/login/"

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ],
}
SWAGGER_SETTINGS = {
    'SECURITY_DEFINITIONS': {
        'Basic': {
            'type': 'basic'
        },
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    }
}

SPECTACULAR_SETTINGS = {
    'TITLE': 'Kvalitātes Dokumentu API',
    'DESCRIPTION': 'API dokumentācija kvalitātes dokumentu pārvaldībai.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'defaultModelRendering': 'model',
        'displayRequestDuration': True,
    },
}
ROSETTA_REQUIRES_SUPERUSER = False
def ROSETTA_ACCESS_CONTROL_FUNCTION(user):
    return True
