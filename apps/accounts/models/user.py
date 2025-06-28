"""
User model for the accounts app.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

class CustomUser(AbstractUser):
    """
    Custom user model for the system.
    Extends Django's AbstractUser to add additional fields and functionality.
    """
    email = models.EmailField(_('email address'), unique=True)
    phone_number = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    
    LANGUAGE_CHOICES = (
        ('en', _('English')),
        ('lv', _('Latvian')),
    )
    
    THEME_CHOICES = (
        ('light', _('Light')),
        ('dark', _('Dark')),
        ('system', _('System Default')),
    )
    
    # Basic user information
    full_name = models.CharField(_("Full Name"), max_length=255, blank=True)
    job_title = models.CharField(_("Job Title"), max_length=100, blank=True)
    
    # Company relationships - ensure these are properly defined with null=True
    company = models.ForeignKey(
        'company.Company',
        on_delete=models.SET_NULL,  # Changed to SET_NULL for safety
        related_name='employees',
        verbose_name=_("Company"),
        null=True,
        blank=True,
    )
    
    department = models.ForeignKey(
        'company.Department',
        on_delete=models.SET_NULL,  # Changed to SET_NULL for safety
        related_name='employees',
        verbose_name=_("Department"),
        null=True,
        blank=True,
    )
    
    # Contact information
    phone = models.CharField(_("Phone Number"), max_length=20, blank=True)
    mobile = models.CharField(_("Mobile Number"), max_length=20, blank=True)
    
    # Preferences
    language = models.CharField(
        _("Preferred Language"),
        max_length=10,
        choices=[
            ('en', _('English')),
            ('lv', _('Latvian')),
            ('ru', _('Russian')),
        ],
        default='en',
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
    
    # Add related names to avoid clashes with auth.User
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name=_('groups'),
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name=_('user permissions'),
        blank=True,
        related_name='customuser_set',
        related_query_name='customuser',
    )
    
    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = _('User')
        verbose_name_plural = _('Users')
