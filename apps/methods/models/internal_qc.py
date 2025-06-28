from django.db import models
from django.utils.translation import gettext_lazy as _


class InternalQualityControl(models.Model):
    """
    Internal Quality Control records for laboratory methods.
    Tracks internal quality assurance procedures and results.
    """
    method = models.ForeignKey(
        'Method',
        on_delete=models.CASCADE,
        related_name='internal_qc_records',
        verbose_name=_('Method')
    )
    control_date = models.DateField(_('Control Date'))
    control_material = models.CharField(_('Control Material'), max_length=255)
    control_lot = models.CharField(_('Control Lot/Batch'), max_length=100, blank=True)
    result = models.CharField(_('Result'), max_length=100)
    expected_value = models.CharField(_('Expected Value'), max_length=100)
    acceptable_range = models.CharField(_('Acceptable Range'), max_length=100, blank=True)
    is_conforming = models.BooleanField(_('Conforms to Expectations'), default=True)
    performed_by = models.CharField(_('Performed By'), max_length=255)
    notes = models.TextField(_('Notes'), blank=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Internal Quality Control')
        verbose_name_plural = _('Internal Quality Controls')
        ordering = ['-control_date']

    def __str__(self):
        return f"{self.method.name} - {self.control_date}"
