"""
User profile model definition.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class UserProfile(models.Model):
    """
    Extended profile information for users.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='accounts_profile',  # Changed from 'profile' to 'accounts_profile'
        verbose_name=_('User')
    )
    bio = models.TextField(
        _('Biography'),
        blank=True,
        help_text=_('A brief description about yourself')
    )
    profile_picture = models.ImageField(
        _('Profile Picture'),
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )
    job_title = models.CharField(
        _('Job Title'),
        max_length=100,
        blank=True
    )
    department = models.CharField(
        _('Department'),
        max_length=100,
        blank=True
    )
    phone_number = models.CharField(
        _('Phone Number'),
        max_length=20,
        blank=True
    )
    date_of_birth = models.DateField(
        _('Date of Birth'),
        blank=True,
        null=True
    )
    city = models.CharField(
        _('City'),
        max_length=100,
        blank=True
    )
    country = models.CharField(
        _('Country'),
        max_length=100,
        blank=True
    )
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
