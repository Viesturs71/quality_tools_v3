from django.db import models
from django.utils.translation import gettext_lazy as _
from typing import ClassVar, List


class Location(models.Model):
    name = models.CharField(_('name'), max_length=255)
    address = models.TextField(_('address'), blank=True, null=True)
    company = models.ForeignKey(
        'company.Company',  # Corrected string reference
        on_delete=models.CASCADE,
        related_name='locations',
        verbose_name=_('company')
    )
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)
    class Meta:
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering: ClassVar[List[str]] = ["name"]
        ordering = ["name"]

    def __str__(self):
        return self.name
