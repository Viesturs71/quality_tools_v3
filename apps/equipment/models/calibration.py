from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings


class CalibrationRecord(models.Model):
    """
    Equipment calibration record
    """
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE, related_name='calibration_records', verbose_name=_('Equipment'))
    performed_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='performed_calibrations', verbose_name=_('Performed By'))
    calibration_date = models.DateField(verbose_name=_('Calibration Date'))
    certificate_number = models.CharField(max_length=100, blank=True, verbose_name=_('Certificate Number'))
    description = models.TextField(verbose_name=_('Description'))
    results = models.TextField(verbose_name=_('Results'))
    passed = models.BooleanField(default=True, verbose_name=_('Passed Calibration'))
    next_calibration_date = models.DateField(null=True, blank=True, verbose_name=_('Next Calibration Date'))
    
    class Meta:
        verbose_name = _('Calibration Record')
        verbose_name_plural = _('Calibration Records')
        ordering = ['-calibration_date']
    
    def __str__(self):
        return f"{_('Calibration')} - {self.equipment.name} ({self.calibration_date})"
    
    def save(self, *args, **kwargs):
        # Update the equipment's next calibration date when saving a calibration record
        if self.next_calibration_date:
            self.equipment.next_calibration_date = self.next_calibration_date
            self.equipment.save(update_fields=['next_calibration_date'])
        super().save(*args, **kwargs)
