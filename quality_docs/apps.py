# quality_docs/apps.py

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class QualityDocsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'quality_docs'
    verbose_name = _('Management Documentation')

    def ready(self):
        try:
            import quality_docs.signals  # Import signals
        except ImportError:
            pass
