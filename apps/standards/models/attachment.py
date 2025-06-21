from django.db import models
from django.utils.translation import gettext_lazy as _
from .standard import Standard


class StandardAttachment(models.Model):
    standard = models.ForeignKey(
        Standard,
        on_delete=models.CASCADE,
        related_name='attachments',
        verbose_name=_('Standard')
    )
    file = models.FileField(_('File'), upload_to='standards/attachments/')
    description = models.TextField(_('Description'), blank=True, null=True)
    uploaded_at = models.DateTimeField(_('Uploaded At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Standard Attachment')
        verbose_name_plural = _('Standard Attachments')

    def __str__(self):
        return f"Attachment for {self.standard}"
