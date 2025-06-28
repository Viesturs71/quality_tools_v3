from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class UserWidgetPosition(models.Model):
    """
    Associates widgets with user preferences and stores position information.
    """
    user_preference = models.ForeignKey(
        'UserPreference',
        on_delete=models.CASCADE,
        related_name='widget_positions',
        verbose_name=_('User Preference')
    )
    widget = models.ForeignKey(
        'Widget',
        on_delete=models.CASCADE,
        related_name='widget_positions',
        verbose_name=_('Widget')
    )
    position_x = models.PositiveSmallIntegerField(_('X Position'), default=0)
    position_y = models.PositiveSmallIntegerField(_('Y Position'), default=0)
    width = models.PositiveSmallIntegerField(_('Width'), default=1)
    height = models.PositiveSmallIntegerField(_('Height'), default=1)
    is_visible = models.BooleanField(_('Visible'), default=True)
    
    class Meta:
        verbose_name = _('Widget Position')
        verbose_name_plural = _('Widget Positions')
        ordering = ['position_y', 'position_x']
        unique_together = ['user_preference', 'widget']
