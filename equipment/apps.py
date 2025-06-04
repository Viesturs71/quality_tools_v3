# equipment/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EquipmentConfig(AppConfig):
    """Configuration for the Equipment app."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "equipment"
    verbose_name = _("Equipment Management")  # This controls the admin sidebar app name

    def ready(self):
        """
        Initialize app when Django starts.
        Connect signals and perform other initialization.
        """
        try:
            # Import and connect signals
            from . import signals
            signals.connect_signals()

        except ImportError as e:
            # Handle case where models aren't loaded yet
            import logging
            logging.getLogger(__name__).warning(
                f"Could not import signals: {e}. This may be normal during migrations."
            )
