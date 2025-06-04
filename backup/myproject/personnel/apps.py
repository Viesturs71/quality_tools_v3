# personnel/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class PersonnelConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'personnel'
    verbose_name = _("Personnel Management")
