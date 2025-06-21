from django.db import models
from django.utils.translation import gettext_lazy as _


class UserPermission(models.Model):
    """
    Custom permissions for user roles.
    """
    role = models.ForeignKey('accounts.UserRole', on_delete=models.CASCADE, related_name='permissions')
    name = models.CharField(_('permission name'), max_length=100)
    codename = models.CharField(_('codename'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('user permission')
        verbose_name_plural = _('user permissions')

    def __str__(self):
        return self.name
