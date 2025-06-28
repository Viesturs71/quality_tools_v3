from django.db import models
from django.utils.translation import gettext_lazy as _

class StandardDocument(models.Model):
    """
    Represents a document that can be linked to standard sections.
    This is a document specifically for standards (as opposed to general documents).
    """
    title = models.CharField(_('Title'), max_length=255)
    description = models.TextField(_('Description'), blank=True)
    file = models.FileField(_('File'), upload_to='standards/documents/')
    document_number = models.CharField(_('Document Number'), max_length=100, blank=True)
    version = models.CharField(_('Version'), max_length=20, blank=True)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=[
            ('draft', _('Draft')),
            ('review', _('Under Review')),
            ('approved', _('Approved')),
            ('published', _('Published')),
            ('obsolete', _('Obsolete')),
        ],
        default='draft'
    )
    is_active = models.BooleanField(_('Is Active'), default=True)
    uploaded_at = models.DateTimeField(_('Uploaded At'), auto_now_add=True)
    uploaded_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='standard_documents',
        verbose_name=_('Uploaded By')
    )
    is_public = models.BooleanField(_('Is Public'), default=False)

    class Meta:
        verbose_name = _('Standard Document')
        verbose_name_plural = _('Standard Documents')
        ordering = ['-uploaded_at', 'title']

    def __str__(self):
        return self.title if not self.document_number else f"{self.title} ({self.document_number})"
