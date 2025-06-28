"""
StandardCategory model for categorizing standards.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class StandardCategory(models.Model):
    """
    Represents a high-level category for grouping standards (e.g., ISO, DIN).
    """
    code = models.CharField(_('Code'), max_length=20, unique=True)
    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Standard Category')
        verbose_name_plural = _('Standard Categories')
        ordering = ['code']

    def __str__(self):
        return f"{self.code} - {self.title}"