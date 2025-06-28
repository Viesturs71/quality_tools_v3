# apps/standards/models/standard_compliance.py

from django.db import models
from django.utils.translation import gettext_lazy as _

class StandardCompliance(models.Model):
    requirement = models.ForeignKey(
        'standards.StandardRequirement',
        on_delete=models.CASCADE,
        related_name='compliance_records',
        verbose_name=_('Requirement')
    )
    user = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        related_name='compliance_records',
        verbose_name=_('User')
    )
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=[
            ('compliant', _('Compliant')),
            ('partial', _('Partially Compliant')),
            ('non_compliant', _('Non-Compliant')),
            ('not_applicable', _('Not Applicable')),
            ('in_progress', _('Implementation in Progress')),
        ],
        default='in_progress'
    )
    notes       = models.TextField(_('Notes'), blank=True)
    recorded_at = models.DateTimeField(_('Recorded At'), auto_now_add=True)

    class Meta:
        verbose_name        = _('Standard Compliance')
        verbose_name_plural = _('Standard Compliances')
        ordering            = ('-recorded_at',)

    def __str__(self):
        # show the full code of the requirement and its status
        return f"{self.requirement.section.standard.code}." \
               f"{self.requirement.code} – {self.get_status_display()}"
