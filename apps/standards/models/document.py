from django.db import models
from django.utils.translation import gettext_lazy as _
from .standard import Standard


class StandardDocument(models.Model):
    standard = models.ForeignKey(
        Standard,
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('Standard')
    )
    title = models.CharField(_('Title'), max_length=255)
    file = models.FileField(_('File'), upload_to='standards/documents/')
    description = models.TextField(_('Description'), blank=True, null=True)
    uploaded_at = models.DateTimeField(_('Uploaded At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Standard Document')
        verbose_name_plural = _('Standard Documents')

    def __str__(self):
        return self.title
