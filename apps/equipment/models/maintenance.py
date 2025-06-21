from django.db import models
from django.contrib.auth.models import User


class MaintenanceRecord(models.Model):
    """
    Equipment maintenance record
    """
    MAINTENANCE_TYPES = (
        ('preventive', 'Profilaktiskā apkope'),
        ('corrective', 'Koriģējošā apkope'),
        ('predictive', 'Prognozējošā apkope'),
        ('emergency', 'Avārijas remonts'),
    )
    
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='maintenance_records', verbose_name='Aprīkojums')
    maintenance_type = models.CharField(max_length=20, choices=MAINTENANCE_TYPES, verbose_name='Apkopes veids')
    performed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='performed_maintenance', verbose_name='Veica')
    performed_date = models.DateField(verbose_name='Veikšanas datums')
    description = models.TextField(verbose_name='Apraksts')
    actions_taken = models.TextField(verbose_name='Veiktās darbības')
    parts_replaced = models.TextField(blank=True, verbose_name='Nomainītās detaļas')
    next_maintenance_date = models.DateField(null=True, blank=True, verbose_name='Nākamās apkopes datums')
    
    class Meta:
        verbose_name = 'Apkopes ieraksts'
        verbose_name_plural = 'Apkopes ieraksti'
        ordering = ['-performed_date']
    
    def __str__(self):
        return f"Apkope - {self.equipment.name} ({self.performed_date})"
    
    def save(self, *args, **kwargs):
        # Update the equipment's next maintenance date when saving a maintenance record
        if self.next_maintenance_date:
            self.equipment.next_maintenance_date = self.next_maintenance_date
            self.equipment.save(update_fields=['next_maintenance_date'])
        super().save(*args, **kwargs)
