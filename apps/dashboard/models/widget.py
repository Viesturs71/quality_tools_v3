from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Widget(models.Model):
    """
    Dashboard widget configuration.
    Widgets are configurable components that can be added to a user's dashboard.
    """
    TYPE_CHOICES = [
        ('chart', _('Chart')),
        ('list', _('List')),
        ('calendar', _('Calendar')),
        ('stats', _('Statistics')),
        ('custom', _('Custom')),
    ]
    
    name = models.CharField(_('Name'), max_length=100)
    widget_type = models.CharField(_('Widget Type'), max_length=20, choices=TYPE_CHOICES)
    description = models.TextField(_('Description'), blank=True)
    config = models.JSONField(_('Configuration'), default=dict, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Widget')
        verbose_name_plural = _('Widgets')
        ordering = ['name']
    
    def __str__(self):
        return self.name
