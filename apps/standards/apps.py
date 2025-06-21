from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StandardsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.standards"
    verbose_name = _("Standards Management")
