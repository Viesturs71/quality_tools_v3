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
    LANGUAGE_CHOICES = (
        ('en', _('English')),
        ('lv', _('Latvian')),
    )
    
    THEME_CHOICES = (
        ('light', _('Light')),
        ('dark', _('Dark')),
        ('system', _('System Default')),
    )
    
    company = models.ForeignKey(
        Company,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    # Add phone_number field if you want to keep it in list_display
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    department = models.ForeignKey(
        'company.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees',
        verbose_name='Department'
    )
    language_preference = models.CharField(
        _('Language Preference'),
        max_length=10,
        choices=LANGUAGE_CHOICES,
        default='en'
    )
    theme_preference = models.CharField(
        _('Theme Preference'),
        max_length=10,
        choices=THEME_CHOICES,
        default='system'
    )

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')

class UserProfile(models.Model):
    """User profile with extended information."""
    user = models.OneToOneField(
        CustomUser,
        on_delete=models.CASCADE,
        related_name='profile',
        verbose_name=_('User')
    )
    bio = models.TextField(_('Biography'), blank=True)
    profile_picture = models.ImageField(
        _('Profile Picture'),
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True)
    address = models.CharField(_('Address'), max_length=255, blank=True)
    job_title = models.CharField(_('Job Title'), max_length=100, blank=True)
    department = models.ForeignKey(
        'company.Department',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('Department')
    )
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
