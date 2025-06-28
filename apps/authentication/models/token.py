from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class Token(models.Model):
    """
    Custom authentication token model for API access.
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='auth_tokens',
        verbose_name=_('User')
    )
    key = models.CharField(_('Key'), max_length=40, unique=True)
    created = models.DateTimeField(_('Created'), auto_now_add=True)
    expires = models.DateTimeField(_('Expires'), blank=True, null=True)
    is_active = models.BooleanField(_('Active'), default=True)
    
    class Meta:
        verbose_name = _('Authentication Token')
        verbose_name_plural = _('Authentication Tokens')
        
    def __str__(self):
        return f"{self.user.username} - {self.key[:10]}..."
