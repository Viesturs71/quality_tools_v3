from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class CustomUser(AbstractUser):
    """
    Custom user model with extended fields
    """
    email = models.EmailField(_('email address'), unique=True)
    
    # Comment out fields that don't exist in the database
    # title = models.CharField(_('title'), max_length=100, blank=True, null=True)
    # phone = models.CharField(_('phone number'), max_length=20, blank=True, null=True)
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        
    def __str__(self):
        return self.username


class UserProfile(models.Model):
    """
    Extended user profile information
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(_('biography'), blank=True, null=True)
    profile_image = models.ImageField(_('profile image'), upload_to='profile_images/', blank=True, null=True)
    job_title = models.CharField(_('job title'), max_length=100, blank=True, null=True)
    department = models.CharField(_('department'), max_length=100, blank=True, null=True)
    language_preference = models.CharField(_('language preference'), max_length=10, default='en')
    theme_preference = models.CharField(_('theme preference'), max_length=20, default='light')
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    
    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')
        
    def __str__(self):
        return f"{self.user.username}'s profile"


class UserRole(models.Model):
    """
    User roles for permission management
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


class UserPermission(models.Model):
    """
    Custom permissions for user roles
    """
    role = models.ForeignKey(UserRole, on_delete=models.CASCADE, related_name='permissions')
    name = models.CharField(_('permission name'), max_length=100)
    codename = models.CharField(_('codename'), max_length=100, unique=True)
    description = models.TextField(_('description'), blank=True, null=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('user permission')
        verbose_name_plural = _('user permissions')
        
    def __str__(self):
        return self.name
