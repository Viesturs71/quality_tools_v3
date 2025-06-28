from django.db import models
from django.utils.translation import gettext_lazy as _
from .audit import Audit


class AuditChecklist(models.Model):
    STATUS_CHOICES = [
        ('compliant', _('Compliant')),
        ('non_compliant', _('Non-Compliant')),
        ('not_applicable', _('Not Applicable')),
        ('not_checked', _('Not Checked')),
    ]

    audit = models.ForeignKey(
        Audit,
        on_delete=models.CASCADE,
        related_name='checklist_items',
        verbose_name=_('Audit')
    )
    question = models.TextField(_('Question'))
    category = models.CharField(_('Category'), max_length=100)
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='not_checked'
    )
    comments = models.TextField(_('Comments'), blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Audit Checklist Item')
        verbose_name_plural = _('Audit Checklist Items')
        ordering = ['category', 'id']
        app_label = 'audits'

    def __str__(self):
        return f"{self.category} - {self.question[:50]}"
