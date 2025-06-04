# accounts/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = _("User Accounts")
    # app_label = "user_accounts"  # Uncomment if there's a conflict

    def ready(self):
        import accounts.signals  # Nodrošina, ka signāli tiek aktivizēti