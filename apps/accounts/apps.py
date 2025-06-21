# accounts/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"  # Corrected path
    verbose_name = _("User Accounts")
    # app_label = "user_accounts"  # Uncomment if there's a conflict

    def ready(self):
        import apps.accounts.signals  # Ensure signals are imported correctly