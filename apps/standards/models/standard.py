from django.db import models
from django.utils.translation import gettext_lazy as _

class Standard(models.Model):
    number = models.CharField(max_length=50, verbose_name=_("Standard Number"))
    title = models.CharField(max_length=255, verbose_name=_("Standard Title"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    revision = models.CharField(blank=True, max_length=20, null=True, verbose_name=_("Revision"))
    issuing_body = models.CharField(blank=True, max_length=100, null=True, verbose_name=_("Issuing Body"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Standard")
        verbose_name_plural = _("Standards")
        ordering = ["number"]

    def __str__(self):
        return self.number
