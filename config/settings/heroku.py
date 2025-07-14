from .base import *

import dj_database_url
import os

# Pārņem datubāzi no DATABASE_URL
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
}

# Static files uzstādījumi Heroku
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATIC_URL = '/static/'

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Whitenoise atļautie faili
if 'whitenoise.middleware.WhiteNoiseMiddleware' not in MIDDLEWARE:
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

# Drošība
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']  # Vai konkrētais heroku domēns
DEBUG = False
