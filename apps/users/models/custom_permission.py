from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomPermission(models.Model):
    """
    Custom permission model for fine-grained access control.
    """
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    codename = models.CharField(_('Code Name'), max_length=100, unique=True, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Custom Permission')
        verbose_name_plural = _('Custom Permissions')
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate codename from name if not provided
        if not self.codename and self.name:
            self.codename = self.name.lower().replace(' ', '_')
        super().save(*args, **kwargs)
