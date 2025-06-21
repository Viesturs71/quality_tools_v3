from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.company.models.company import Company  # Updated import
from apps.company.models.department import Department  # Updated import


class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='custom_users',  # Added related_name
        verbose_name=_('Company')  # Already in English
    )
    phone_number = models.CharField(
        _('Phone Number'), max_length=20, blank=True, null=True  # Already in English
    )
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='custom_users',  # Added related_name
        verbose_name=_('Department')  # Already in English
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # Added related_name
        blank=True,
        help_text=_('The groups this user belongs to.'),
        verbose_name=_('Groups'),
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # Added related_name
        blank=True,
        help_text=_('Specific permissions for this user.'),
        verbose_name=_('User Permissions'),
    )

    def __str__(self):
        return self.username
