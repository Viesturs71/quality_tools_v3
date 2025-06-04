from django.db import models
from django.utils.translation import gettext_lazy as _


class EquipmentType(models.Model):
    """
    Model representing types of equipment and measuring instruments.
    """
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    requires_metrological_control = models.BooleanField(_('Requires Metrological Control'), default=False)
    requires_maintenance = models.BooleanField(_('Requires Maintenance'), default=True)
    maintenance_period = models.IntegerField(_('Maintenance Period (days)'), default=365)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Equipment Type')
        verbose_name_plural = _('Equipment Types')
        ordering = ['name']
