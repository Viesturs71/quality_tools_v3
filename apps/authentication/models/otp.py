from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
import random
import string


class OneTimePassword(models.Model):
    """
    One-time password for two-factor authentication.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='one_time_passwords',
        verbose_name=_('User')
    )
    code = models.CharField(_('Code'), max_length=6)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    expires_at = models.DateTimeField(_('Expires at'))
    is_used = models.BooleanField(_('Used'), default=False)
    
    class Meta:
        verbose_name = _('One-Time Password')
        verbose_name_plural = _('One-Time Passwords')
    
    def __str__(self):
        return f"OTP for {self.user.username}"
    
    @classmethod
    def generate_code(cls):
        """Generate a 6-digit code for OTP."""
        return ''.join(random.choices(string.digits, k=6))
