# methods/models/eqc.py
from django.db import models
from django.utils.translation import gettext_lazy as _


class ExternalQualityControl(models.Model):
    """
    External Quality Control (EQC) registry for recording external quality assessments.
    """
    service_provider = models.CharField(max_length=255, verbose_name=_("Service Provider"))
    laboratory = models.CharField(max_length=255, verbose_name=_("Laboratory"))
    code = models.CharField(max_length=100, verbose_name=_("Code"))
    test_material = models.CharField(max_length=255, verbose_name=_("Test Material"))
    technology_examination = models.CharField(max_length=255, verbose_name=_("Technology/Examination"))
    quantity = models.PositiveIntegerField(verbose_name=_("Quantity"))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Price (€)"))
    test_amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_("Test Amount (€)"))
    
    # Optional relationship to Method
    method = models.ForeignKey(
        'Method',
        on_delete=models.SET_NULL,
        related_name='external_quality_controls',
        verbose_name=_("Method"),
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = _("External Quality Control")
        verbose_name_plural = _("External Quality Controls")
        ordering = ["service_provider", "laboratory"]

    def __str__(self):
        return f"{self.service_provider} - {self.laboratory} ({self.code})"
