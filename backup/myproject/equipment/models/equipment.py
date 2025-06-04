from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Equipment(models.Model):
    """
    Model representing equipment and measuring instruments.
    """

    equipment_name = models.CharField(_("Equipment Name"), max_length=255)
    inventory_number = models.CharField(
        _("Inventory Number"), max_length=50, unique=True
    )
    serial_number = models.CharField(_("Serial Number"), max_length=50)
    model = models.CharField(_("Model"), max_length=100, blank=True, null=True)
    manufacturer = models.CharField(
        _("Manufacturer"), max_length=100, blank=True, null=True
    )
    equipment_type = models.ForeignKey(
        "EquipmentType",
        on_delete=models.CASCADE,
        related_name="equipment",
        verbose_name=_("Equipment Type"),
    )
    location = models.CharField(_("Location"), max_length=100)
    department = models.ForeignKey(
        "Department",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="equipment_items",
        verbose_name=_("Department"),
    )
    person_responsible = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Responsible person",
    )
    manufacture_date = models.DateField(_("Manufacture Date"), null=True, blank=True)
    purchase_date = models.DateField(_("Purchase Date"), null=True, blank=True)
    purchase_price = models.DecimalField(
        _("Purchase Price"), max_digits=10, decimal_places=2, null=True, blank=True
    )

    # Metrological control fields
    metrological_control_type = models.CharField(
        _("Metrological Control Type"), max_length=100, blank=True, null=True
    )
    metrological_control_institution = models.CharField(
        _("Metrological Control Institution"), max_length=100, blank=True, null=True
    )
    certificate_number = models.CharField(
        _("Certificate Number"), max_length=100, blank=True, null=True
    )
    certificate_date = models.DateField(_("Certificate Date"), null=True, blank=True)
    metrological_control_periodicity = models.IntegerField(
        _("Metrological Control Periodicity (months)"), null=True, blank=True
    )
    next_verification_date = models.DateField(
        _("Next Verification Date"), null=True, blank=True
    )

    # Status fields
    technical_status = models.CharField(
        _("Technical Status"), max_length=50, default="Good"
    )
    additional_information = models.TextField(
        _("Additional Information"), blank=True, null=True
    )
    notes = models.TextField(_("Notes"), blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(
        _("Created At"), default=timezone.now, editable=False
    )
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    def __str__(self):
        return f"{self.equipment_name} ({self.inventory_number})"

    class Meta:
        verbose_name = _("Equipment")
        verbose_name_plural = _("Equipment")
        ordering = ["equipment_name"]
