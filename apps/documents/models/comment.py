from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class DocumentComment(models.Model):
    """Model representing comments on documents."""
    document = models.ForeignKey('Document', on_delete=models.CASCADE, related_name='comments', verbose_name=_('Document'))
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('Author'))
    text = models.TextField(verbose_name=_('Comment'))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Created At'))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_('Updated At'))
    
    class Meta:
        verbose_name = _('Document Comment')
        verbose_name_plural = _('Document Comments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment from {self.author.username} about {self.document.document_number}"
