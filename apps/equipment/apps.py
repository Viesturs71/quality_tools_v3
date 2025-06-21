from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EquipmentConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.equipment"
    verbose_name = _("Equipment Management")

    def ready(self):
        """
        Initialize app when Django starts.
        Connect signals and perform other initialization.
        """
        from . import signals

        signals.connect_signals()  # Ensure this function exists in signals.py
