# equipment/models/equipment_registry.py
import datetime

from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class EquipmentRegistry(models.Model):
    """
    Model representing an equipment registry entry.
    This can be used to track equipment across different departments or locations.
    """

    # --- pamata lauki ---------------------------------------------------------
    equipment = models.ForeignKey(
        'Equipment',
        on_delete=models.CASCADE,
        related_name='registry_entries',
        verbose_name=_('Equipment')
    )
    registration_date = models.DateField(_('Registration Date'), default=timezone.now)
    registration_number = models.CharField(_('Registration Number'), max_length=50, unique=True)
    status = models.CharField(_('Status'), max_length=50, default='Active')
    notes = models.TextField(_('Notes'), blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created At'), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    # --- verifikācija / kalibrēšana ------------------------------------------
    INSPECTION_CHOICES = [
        ("C", _("Calibration")),
        ("V", _("Verification")),
        ("MT", _("Maintenance")),
        ("IT", _("Inspection Test")),
    ]
    inspection_type = models.CharField(
        _("Metrological Inspection Type"), max_length=2, choices=INSPECTION_CHOICES, default="C"
    )
    inspection_institution = models.CharField(
        _("Metrological Inspection Institution, Country"),
        max_length=200,
        blank=True,
        default="Not specified",
    )
    certificate_number_date = models.CharField(
        _("Metrological Inspection Certificate Number and Date"),
        max_length=200,
        default="Not specified",
    )
    inspection_frequency = models.CharField(
        _("Metrological Inspection Frequency"), max_length=100, default="Not specified"
    )
    next_inspection_date = models.DateField(_("Next Inspection Date"), null=True, blank=True)

    # -------------------------------------------------------------------------
    class Meta:
        app_label = 'equipment'
        verbose_name = _("Equipment Registry")
        verbose_name_plural = _("Equipment Registry")
        ordering = ["next_inspection_date"]

    # -------------------------------------------------------------------------
    def __str__(self):
        return f"{self.equipment.equipment_name} - {self.registration_number}"

    def get_absolute_url(self):
        return reverse("equipment:detail", kwargs={"pk": self.pk})

    # -------------------------------------------------------------------------
    # biznesa loģika / validācija
    def is_inspection_valid(self):
        return bool(self.next_inspection_date and self.next_inspection_date >= datetime.date.today())

    def clean(self):
        if self.next_inspection_date and self.next_inspection_date < datetime.date.today():
            raise ValidationError(
                {"next_inspection_date": _("The next inspection date cannot be in the past.")}
            )

    def save(self, *args, **kwargs):
        self.inventory_number = (self.inventory_number or "").strip().upper()
        super().save(*args, **kwargs)
