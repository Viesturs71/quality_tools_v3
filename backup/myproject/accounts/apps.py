# accounts/apps.py
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"
    verbose_name = _("User Accounts")  # ✅ Angļu valodā💡 Piešķir tulkojumu Django admin panelī

    def ready(self):
        """
        Django signāli tiek importēti šeit, lai nodrošinātu, ka tie tiek reģistrēti
        tikai pēc tam, kad Django lietotne ir pilnībā ielādēta.
        """
