from django.db import models
from django.utils.translation import gettext_lazy as _
from .audit import Audit


class AuditFinding(models.Model):
    SEVERITY_CHOICES = [
        ('critical', _('Critical')),
        ('major', _('Major')),
        ('minor', _('Minor')),
        ('observation', _('Observation')),
    ]

    audit = models.ForeignKey(
        Audit,
        on_delete=models.CASCADE,
        related_name='findings',
        verbose_name=_('Audit')
    )
    description = models.TextField(_('Description'))
    severity = models.CharField(
        _('Severity'),
        max_length=20,
        choices=SEVERITY_CHOICES,
        default='minor'
    )
    reference = models.CharField(_('Reference'), max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Audit Finding')
        verbose_name_plural = _('Audit Findings')
        ordering = ['severity', 'created_at']
        app_label = 'audits'

    def __str__(self):
        return f"{self.get_severity_display()} - {self.description[:50]}"
