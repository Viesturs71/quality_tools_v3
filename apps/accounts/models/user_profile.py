from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class UserProfile(models.Model):
    """
    Extended user profile information.
    """
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='account_profile', verbose_name=_('User'))
    bio = models.TextField(_('biography'), blank=True, null=True)
    profile_image = models.ImageField(_('Profile Image'), upload_to='profiles/', blank=True, null=True)
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
