from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserPreference(models.Model):
    """
    User dashboard preferences.
    Stores user-specific settings for dashboard layout and widgets.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='dashboard_preferences',
        verbose_name=_('User')
    )
    layout = models.JSONField(_('Layout'), default=dict)
    theme = models.CharField(_('Theme'), max_length=20, default='light')
    widgets = models.ManyToManyField(
        'dashboard.Widget',
        through='UserWidgetPosition',
        related_name='user_preferences',
        verbose_name=_('Widgets')
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('User Preference')
        verbose_name_plural = _('User Preferences')
    
    def __str__(self):
        return f"{self.user.username}'s preferences"


