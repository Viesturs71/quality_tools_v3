# apps/standards/models/standard_document_link.py
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

class StandardDocumentLink(models.Model):
    COMPLIANCE_CHOICES = [
        ('compliant', _('Compliant')),
        ('partial', _('Partially compliant')),
        ('non_compliant', _('Non-compliant')),
        ('not_applicable', _('Not applicable')),
        ('in_progress', _('Implementation in progress')),
    ]

    standard_section = models.ForeignKey(
        'apps.standards.StandardSection',
        related_name='document_links',
        on_delete=models.CASCADE
    )
    document = models.ForeignKey(
        'apps.standards.StandardDocument',
        related_name='standard_links',
        on_delete=models.CASCADE
    )
    compliance_status = models.CharField(
        max_length=20,
        choices=COMPLIANCE_CHOICES,
        default='in_progress'
    )
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        on_delete=models.SET_NULL
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Section Document Link')
        verbose_name_plural = _('Section Document Links')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.standard_section} ↔ {self.document} ({self.compliance_status})"