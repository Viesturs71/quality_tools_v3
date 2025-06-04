from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class MaintenanceRecord(models.Model):
    """
    Model representing a maintenance record for equipment.
    """
    equipment = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        related_name='maintenance_records',
        verbose_name=_('Equipment')
    )
    maintenance_type = models.CharField(_('Maintenance Type'), max_length=100)
    date_performed = models.DateField(_('Date Performed'))
    performed_by = models.CharField(_('Performed By'), max_length=100)
    result = models.CharField(_('Result'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    next_maintenance_date = models.DateField(_('Next Maintenance Date'), null=True, blank=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created At'), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    def __str__(self):
        return f"{self.equipment.equipment_name} - {self.maintenance_type} on {self.date_performed}"

    class Meta:
        verbose_name = _('Maintenance Record')
        verbose_name_plural = _('Maintenance Records')
        ordering = ['-date_performed']
