from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _  # Import gettext_lazy for translations


class CompanyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.company'  # Ensure this matches the app's path
    verbose_name = _('Company Management')  # Use the imported _ function for translations

    def ready(self):
        # Import signals here if needed
        pass
