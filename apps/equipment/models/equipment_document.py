from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class EquipmentDocument(models.Model):
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='documents', verbose_name=_('Equipment'))
    title = models.CharField(_('Title'), max_length=255)
    document = models.FileField(upload_to='equipment_documents/', verbose_name=_('Document'))
    description = models.TextField(_('Description'), blank=True, null=True)
    uploaded_at = models.DateTimeField(_('Uploaded At'), auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='equipment_document_uploaded_by',  # Unique related_name
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _('Equipment Document')
        verbose_name_plural = _('Equipment Documents')
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title
