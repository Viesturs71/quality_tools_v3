"""
User permissions model for the accounts app.
Defines permission settings for users in the system.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()

class UserPermission(models.Model):
    """
    Model to store additional permissions for users beyond Django's built-in permissions.
    This allows for more granular control of user access to different parts of the system.
    """
    user = models.ForeignKey(
        User,  # Using Django's get_user_model() for flexibility
        on_delete=models.CASCADE,
        related_name='custom_permissions',
        verbose_name=_('User')
    )
    
    # Permission settings
    can_approve_documents = models.BooleanField(
        _('Can approve documents'),
        default=False,
        help_text=_('Allow user to approve documents')
    )
    
    can_manage_users = models.BooleanField(
        _('Can manage users'),
        default=False,
        help_text=_('Allow user to create and modify other users')
    )
    
    can_export_data = models.BooleanField(
        _('Can export data'),
        default=False,
        help_text=_('Allow user to export data from the system')
    )
    
    # Metadata
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('User Permission')
        verbose_name_plural = _('User Permissions')
        unique_together = ('user',)  # Each user should have only one permission record
    
    def __str__(self):
        return f'Permissions for {self.user.username}'
