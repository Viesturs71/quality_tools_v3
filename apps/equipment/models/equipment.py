from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.company.models import Department  # Ensure this import is correct
from .equipment_type import EquipmentType  # Import EquipmentType from its own file
from apps.documents.models import Document  # Updated from apps.quality_docs.models

User = get_user_model()  # Import the User model dynamically


class Equipment(models.Model):
    """
    Equipment/instrument model for quality management system
    """
    STATUS_CHOICES = [
        ('active', _("Active")),
        ('inactive', _("Inactive")),
        ('under_repair', _("Under Repair")),
        ('decommissioned', _("Decommissioned")),
    ]

    name = models.CharField(_("Name"), max_length=255)
    equipment_type = models.ForeignKey(EquipmentType, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Equipment Type"))
    inventory_number = models.CharField(_("Inventory Number"), max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Department"))
    responsible_person = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='responsible_for_equipment',
        verbose_name=_("Responsible Person")
    )
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='active')

    description = models.TextField(blank=True, verbose_name=_('Description'))
    manufacturer = models.CharField(max_length=100, blank=True, verbose_name=_('Manufacturer'))
    model_number = models.CharField(max_length=100, blank=True, verbose_name=_('Model Number'))
    serial_number = models.CharField(max_length=100, blank=True, verbose_name=_('Serial Number'))
    purchase_date = models.DateField(null=True, blank=True, verbose_name=_('Purchase Date'))
    needs_calibration = models.BooleanField(default=False, verbose_name=_('Needs Calibration'))
    calibration_frequency = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Calibration Frequency (days)'))
    next_calibration_date = models.DateField(null=True, blank=True, verbose_name=_('Next Calibration Date'))
    
    class Meta:
        verbose_name = _("Equipment")
        verbose_name_plural = _("Equipment")
        ordering = ['name']
    
    def __str__(self):
        return f"{self.name} ({self.inventory_number})"
