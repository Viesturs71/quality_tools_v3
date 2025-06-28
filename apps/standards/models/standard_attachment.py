from django.db import models
from django.utils.translation import gettext_lazy as _

class StandardAttachment(models.Model):
    """
    Represents an attachment (file or URL) to a standard section.
    """
    section = models.ForeignKey(
        'standards.StandardSection',
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_('Section')
    )
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    file = models.FileField(
        _('File'),
        upload_to='standards/attachments/',
        null=True,
        blank=True
    )
    url = models.URLField(
        _('URL'),
        max_length=500,
        null=True,
        blank=True
    )
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='standard_attachments',
        verbose_name=_('Created By')
    )

    class Meta:
        verbose_name = _('Standard Attachment')
        verbose_name_plural = _('Standard Attachments')
        ordering = ['section', 'title']

    def __str__(self):
        return f"{self.title} ({self.section})"
    
    def clean(self):
        """Ensure that either file or URL is provided, but not both."""
        from django.core.exceptions import ValidationError
        
        if not self.file and not self.url:
            raise ValidationError(_('Either a file or URL must be provided.'))
        
        if self.file and self.url:
            raise ValidationError(_('Please provide either a file or URL, not both.'))
