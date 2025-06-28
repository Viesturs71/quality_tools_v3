from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AuditsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.audits'
    verbose_name = _('Audits')
