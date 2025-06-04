import os

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


def equipment_document_path(instance, filename):
    """
    Generate file path for equipment documents.
    Format: equipment_docs/{equipment_id}/{document_type}/{filename}
    """
    ext = filename.split('.')[-1]
    new_filename = f"{instance.id}.{ext}" if instance.id else filename
    return f"equipment_docs/{instance.equipment.id}/{instance.document_type}/{new_filename}"

class EquipmentDocument(models.Model):
    """
    Model representing documents attached to equipment.
    """
    DOCUMENT_TYPES = [
        ('user_manual', _('User Manual')),
        ('certificate', _('Certificate')),
        ('calibration', _('Calibration Document')),
        ('maintenance', _('Maintenance Record')),
        ('warranty', _('Warranty')),
        ('other', _('Other')),
    ]

    equipment = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        related_name='documents',
        verbose_name=_('Equipment')
    )
    document_type = models.CharField(_('Document Type'), max_length=20, choices=DOCUMENT_TYPES)
    title = models.CharField(_('Title'), max_length=200)
    file = models.FileField(_('File'), upload_to=equipment_document_path, blank=True, null=True)
    external_url = models.URLField(_('External URL'), blank=True, null=True)
    internal_reference = models.CharField(_('Internal Reference'), max_length=100, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created At'), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    def __str__(self):
        return f"{self.title} ({self.get_document_type_display()})"

    class Meta:
        verbose_name = _('Equipment Document')
        verbose_name_plural = _('Equipment Documents')
        ordering = ['document_type', 'title']

    def clean(self):
        """
        Validate that at least one of file or external_url is provided.
        """
        if not self.file and not self.external_url and not self.internal_reference:
            raise models.ValidationError(_('At least one of File, External URL, or Internal Reference must be provided.'))

    def delete(self, *args, **kwargs):
        """
        Delete associated file when document is deleted.
        """
        if self.file:
            if os.path.isfile(self.file.path):
                os.remove(self.file.path)
        super().delete(*args, **kwargs)
