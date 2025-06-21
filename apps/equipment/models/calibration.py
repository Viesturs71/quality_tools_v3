from django.db import models
from django.contrib.auth.models import User


class CalibrationRecord(models.Model):
    """
    Equipment calibration record
    """
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='calibration_records', verbose_name='Aprīkojums')
    performed_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='performed_calibrations', verbose_name='Veica')
    calibration_date = models.DateField(verbose_name='Kalibrācijas datums')
    certificate_number = models.CharField(max_length=100, blank=True, verbose_name='Sertifikāta numurs')
    description = models.TextField(verbose_name='Apraksts')
    results = models.TextField(verbose_name='Rezultāti')
    passed = models.BooleanField(default=True, verbose_name='Izturēja kalibrāciju')
    next_calibration_date = models.DateField(null=True, blank=True, verbose_name='Nākamās kalibrācijas datums')
    
    class Meta:
        verbose_name = 'Kalibrācijas ieraksts'
        verbose_name_plural = 'Kalibrācijas ieraksti'
        ordering = ['-calibration_date']
    
    def __str__(self):
        return f"Kalibrācija - {self.equipment.name} ({self.calibration_date})"
    
    def save(self, *args, **kwargs):
        # Update the equipment's next calibration date when saving a calibration record
        if self.next_calibration_date:
            self.equipment.next_calibration_date = self.next_calibration_date
            self.equipment.save(update_fields=['next_calibration_date'])
        super().save(*args, **kwargs)
