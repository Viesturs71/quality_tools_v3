from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class MaintenanceRecord(models.Model):
    MAINTENANCE_TYPE_CHOICES = [
        ('routine', _('Routine Maintenance')),
        ('repair', _('Repair')),
        ('calibration', _('Calibration')),
        ('inspection', _('Inspection')),
        ('upgrade', _('Upgrade/Modification')),
        ('other', _('Other')),
    ]

    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='maintenance_records', verbose_name=_('Equipment'))
    maintenance_date = models.DateField(_('Maintenance Date'), default=timezone.now)
    maintenance_type = models.CharField(_('Maintenance Type'), max_length=20, choices=MAINTENANCE_TYPE_CHOICES, default='routine')
    performed_by = models.CharField(_('Performed By'), max_length=255)
    description = models.TextField(_('Description'))
    next_maintenance_date = models.DateField(_('Next Maintenance Date'), blank=True, null=True)

    class Meta:
        verbose_name = _('Maintenance Record')
        verbose_name_plural = _('Maintenance Records')
        ordering = ['-maintenance_date']

    def __str__(self):
        return f"{self.get_maintenance_type_display()} on {self.maintenance_date}"
