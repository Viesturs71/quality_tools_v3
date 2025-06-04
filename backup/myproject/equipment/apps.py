# equipment/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EquipmentConfig(AppConfig):
    """Configuration for the Equipment app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "equipment"
    verbose_name = _("Equipment Management")  # This controls the admin sidebar app name

    def ready(self):
        """Import signals when the app is ready."""
        try:
            import equipment.signals  # noqa F401
        except ImportError:
            pass
