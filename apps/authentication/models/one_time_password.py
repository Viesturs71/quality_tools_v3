from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
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
        verbose_name=_('User'),
        db_index=True  # Add index for performance
    )
    code = models.CharField(_('Code'), max_length=6, db_index=True)  # Add index for lookups
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    expires_at = models.DateTimeField(_('Expires at'))
    is_used = models.BooleanField(_('Used'), default=False)
    
    class Meta:
        verbose_name = _('One-Time Password')
        verbose_name_plural = _('One-Time Passwords')
        indexes = [
            models.Index(fields=['user', 'code']),
            models.Index(fields=['created_at']),
            models.Index(fields=['expires_at']),
        ]
    
    def save(self, *args, **kwargs):
        """Auto-generate code and expiry if not set."""
        if not self.code:
            self.code = self.generate_code()
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=5)  # 5 minute expiry
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"OTP for {self.user.username} - {self.code}"
    
    @classmethod
    def generate_code(cls):
        """Generate a 6-digit code for OTP."""
        return ''.join(random.choices(string.digits, k=6))
    
    def is_valid(self):
        """Check if the OTP is valid (not used and not expired)."""
        return not self.is_used and timezone.now() <= self.expires_at