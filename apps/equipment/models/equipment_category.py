from django.db import models
from django.utils.translation import gettext_lazy as _


class EquipmentCategory(models.Model):
    name = models.CharField(_('Category Name'), max_length=100, unique=True)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name = _('Equipment Category')
        verbose_name_plural = _('Equipment Categories')
        ordering = ['name']

    def __str__(self):
        return self.name
