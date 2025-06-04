from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from company.models import Company


class User(AbstractUser):
    """
    Custom user model to provide additional functionality.
    Using the AbstractUser as base to retain all Django's default user fields.
    """
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)

    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='employees',
        verbose_name=_('Company'),
        null=True,
        blank=True
    )

    groups = models.ManyToManyField(
        "auth.Group",
        related_name="accounts_users",
        blank=True,
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        related_name="accounts_user_permissions",
        blank=True,
    )

    class Meta:
        db_table = "accounts_user"
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

class CustomUser(AbstractUser):
    """
    Custom user model extending Django's AbstractUser.
    """
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    # Add phone_number field if you want to keep it in list_display
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.username
