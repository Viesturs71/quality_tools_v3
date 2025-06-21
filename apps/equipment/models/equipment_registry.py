from django.db import models
from django.utils.translation import gettext_lazy as _
from .equipment import Equipment
from apps.personnel.models import Employee  # Ensure Employee is imported correctly
from apps.users.models import Profile  # Update this import to reference the correct app


class EquipmentRegistry(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, verbose_name=_("Equipment"))
    authorized_user = models.ForeignKey(Employee, on_delete=models.CASCADE, verbose_name=_("Authorized User"))
    authorized_since = models.DateField(_("Authorized Since"), null=True, blank=True)
    authorized_until = models.DateField(_("Authorized Until"), null=True, blank=True)
    status = models.CharField(
        _("Status"),
        max_length=50,
        choices=[
            ('active', _("Active")),
            ('inactive', _("Inactive")),
            ('maintenance', _("Maintenance")),
        ],
        default='active',
    )
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        verbose_name = _("Equipment Registry Entry")
        verbose_name_plural = _("Equipment Registry")
        unique_together = ('equipment', 'authorized_user')

    def __str__(self):
        return f"{self.equipment} - {self.authorized_user}"
