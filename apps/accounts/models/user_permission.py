from django.db import models
from django.utils.translation import gettext_lazy as _


class UserPermission(models.Model):
    """Custom user permission model for more granular control."""

    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.CASCADE,
        related_name='custom_permissions',
        verbose_name=_('User')
    )

    resource = models.CharField(
        _('Resource'),
        max_length=100,
        help_text=_('The resource this permission applies to')
    )

    permission_type = models.CharField(
        _('Permission Type'),
        max_length=50,
        choices=[
            ('view', _('View')),
            ('add', _('Add')),
            ('change', _('Change')),
            ('delete', _('Delete')),
            ('approve', _('Approve')),
            ('assign', _('Assign')),
        ],
        help_text=_('The type of permission granted')
    )

    module = models.CharField(
        _('Module'),
        max_length=50,
        help_text=_('The module this permission belongs to')
    )

    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('User Permission')
        verbose_name_plural = _('User Permissions')
        unique_together = ('user', 'resource', 'permission_type')
        ordering = ('user', 'module', 'resource')

    def __str__(self):
        return f"{self.user.username} - {self.resource} - {self.get_permission_type_display()}"
