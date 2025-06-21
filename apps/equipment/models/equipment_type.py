from django.db import models
from django.utils.translation import gettext_lazy as _


class EquipmentType(models.Model):
    name = models.CharField(_('Type Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    is_measuring_instrument = models.BooleanField(_('Is Measuring Instrument'), default=False)
    requires_metrological_control = models.BooleanField(_('Requires Metrological Control'), default=False)
    is_active = models.BooleanField(_('Active'), default=True)

    class Meta:
        verbose_name = _('Equipment Type')
        verbose_name_plural = _('Equipment Types')
        ordering = ['name']

    def __str__(self):
        return self.name
