from django.db import models
from django.utils.translation import gettext_lazy as _


class Attachment(models.Model):
    """
    A file attachment linked to a document.
    """
    document = models.ForeignKey(
        'documents.Document',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_('Document')
    )
    file = models.FileField(
        _('File'),
        upload_to='documents/attachments/'
    )
    description = models.CharField(
        _('Description'),
        max_length=255,
        blank=True
    )
    uploaded_at = models.DateTimeField(
        _('Uploaded At'),
        auto_now_add=True
    )
    
    class Meta:
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')
        ordering = ['-uploaded_at']
        
    def __str__(self):
        return f"{self.document.title} - {self.file.name}"
