"""
ASGI config for Quality Tools project.
"""
import os

from django.core.asgi import get_asgi_application

# Set the default Django settings module for the 'asgi' application
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.prod')

application = get_asgi_application()
