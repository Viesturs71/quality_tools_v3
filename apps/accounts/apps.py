# accounts/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    verbose_name = _("User Accounts")

    def ready(self):
        import apps.accounts.signals  # Import signals with correct package path