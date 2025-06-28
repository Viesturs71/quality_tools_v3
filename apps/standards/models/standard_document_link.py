# apps/standards/models/standard_document_link.py

from django.db import models
from django.utils.translation import gettext_lazy as _

class StandardDocumentLink(models.Model):
    standard_section = models.ForeignKey(
        'standards.StandardSection',
        on_delete=models.CASCADE,
        related_name='document_links',
        verbose_name=_('Standard Section'),
    )
    document = models.ForeignKey(
        'standards.StandardDocument',
        on_delete=models.CASCADE,
        related_name='standard_links',
        verbose_name=_('Document'),
    )
    compliance_status = models.CharField(
        _('Compliance Status'),
        max_length=20,
        choices=[
            ('compliant', _('Compliant')),
            ('partial', _('Partially Compliant')),
            ('non_compliant', _('Non-Compliant')),
            ('not_applicable', _('Not Applicable')),
            ('in_progress', _('Implementation in Progress')),
        ],
        default='compliant',
    )
    notes      = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    created_by = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_standard_links',
        verbose_name=_('Created By'),
    )

    class Meta:
        verbose_name        = _('Standard-Document Link')
        verbose_name_plural = _('Standard-Document Links')
        unique_together     = ('standard_section', 'document')
        ordering            = ('standard_section__code', 'document__title')

    def __str__(self):
        return f"{self.standard_section.code} → {self.document.title}"
