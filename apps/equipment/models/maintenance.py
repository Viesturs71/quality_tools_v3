from django.db import models
from django.utils.translation import gettext_lazy as _


class MaintenanceRecord(models.Model):
    """
    Equipment maintenance record
    """
    MAINTENANCE_TYPES = (
        ('preventive', _('Preventive Maintenance')),
        ('corrective', _('Corrective Maintenance')),
        ('predictive', _('Predictive Maintenance')),
        ('emergency', _('Emergency Repair')),
    )
    
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='maintenance_records', verbose_name=_('Equipment'))
    date = models.DateField(_("Maintenance Date"))  # This should be 'date', not 'maintenance_date'
    maintenance_type = models.CharField(
        _("Maintenance Type"),
        max_length=20,
        choices=MAINTENANCE_TYPES,
        default='preventive'
    )
    description = models.TextField(_("Description"))
    performed_by = models.ForeignKey(
        'personnel.Employee',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='performed_maintenance',
        verbose_name=_("Performed By")
    )
    cost = models.DecimalField(
        _("Cost"),
        max_digits=10, 
        decimal_places=2,
        null=True,
        blank=True
    )
    notes = models.TextField(_("Notes"), blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Maintenance Record")
        verbose_name_plural = _("Maintenance Records")
        ordering = ['-date']

    def __str__(self):
        return f"{self.equipment.name} - {self.get_maintenance_type_display()} ({self.date})"
    
    def save(self, *args, **kwargs):
        # Update the equipment's next maintenance date when saving a maintenance record
        if self.next_maintenance_date:
            self.equipment.next_maintenance_date = self.next_maintenance_date
            self.equipment.save(update_fields=['next_maintenance_date'])
        super().save(*args, **kwargs)
