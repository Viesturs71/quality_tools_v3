from django.db import models
from django.utils.translation import gettext_lazy as _


class UserRole(models.Model):
    """
    User roles for permission management.
    """
    name = models.CharField(_('role name'), max_length=100)
    description = models.TextField(_('description'), blank=True, null=True)
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        verbose_name = _('user role')
        verbose_name_plural = _('user roles')

    def __str__(self):
        return self.name
