from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# Update import to get Department from company.py
from company.models.company import Department
from personnel.models import Employee
from django.contrib.auth import get_user_model
from django.conf import settings

User = get_user_model()

class EquipmentType(models.Model):
    name = models.CharField(_('Type Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    is_measuring_instrument = models.BooleanField(_('Is Measuring Instrument'), default=False)
    maintenance_interval = models.PositiveIntegerField(_('Maintenance Interval (days)'), null=True, blank=True)
    maintenance_procedure = models.TextField(_('Maintenance Procedure'), blank=True, null=True)
    metrological_control_required = models.BooleanField(_('Metrological Control Required'), default=False)
    standard_control_interval = models.PositiveIntegerField(_('Standard Control Interval (months)'), null=True, blank=True)
    is_active = models.BooleanField(_('Active'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    def __str__(self):
        return f"{self.name} ({_('Measuring Instrument') if self.is_measuring_instrument else _('Equipment')})"

    class Meta:
        verbose_name = _('Equipment Type')
        verbose_name_plural = _('Equipment Types')
        ordering = ['name']
        indexes = [
            models.Index(fields=['name'], name='eq_type_name_idx'),
            models.Index(fields=['is_measuring_instrument'], name='eq_type_meas_idx'),
            models.Index(fields=['is_active'], name='eq_type_active_idx'),
        ]


class Department(models.Model):
    name = models.CharField(_('Department Name'), max_length=100)
    company = models.ForeignKey('company.Company', on_delete=models.CASCADE)
    location = models.ForeignKey('company.Location', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name']
class EquipmentLocation(models.Model):
    name = models.CharField(max_length=255)  # piemēram, "Cehs A", "3. stāva laboratorija"
    floor = models.CharField(max_length=20, blank=True, null=True)
    building = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(_("Name"), max_length=255)
    equipment_type = models.ForeignKey('EquipmentType', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Equipment Type"))
    model = models.CharField(_("Model"), max_length=255, blank=True)
    type_details = models.TextField(_("Type Details"), blank=True)
    manufacturer = models.CharField(_("Manufacturer"), max_length=255, blank=True)
    inventory_number = models.CharField(_("Inventory Number"), max_length=100, unique=True)
    serial_number = models.CharField(_("Serial Number"), max_length=100, blank=True)
    location = models.ForeignKey('equipment.EquipmentLocation', on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Location"))
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Department"))
    responsible_person = models.CharField(_("Responsible Person"), max_length=255, blank=True)
    manufacture_date = models.DateField(_("Manufacture Date"), null=True, blank=True)
    purchase_date = models.DateField(_("Purchase Date"), null=True, blank=True)
    purchase_price = models.DecimalField(_("Purchase Price"), max_digits=10, decimal_places=2, null=True, blank=True)
    is_measuring_instrument = models.BooleanField(_("Is Measuring Instrument"), default=False)
    metrological_control_type = models.CharField(_("Metrological Control Type"), max_length=255, blank=True)
    metrological_control_institution = models.CharField(_("Metrological Control Institution"), max_length=255, blank=True)
    certificate_number = models.CharField(_("Certificate Number"), max_length=100, blank=True)
    certificate_date = models.DateField(_("Certificate Date"), null=True, blank=True)
    control_periodicity = models.PositiveIntegerField(_("Control Periodicity (months)"), null=True, blank=True)
    next_verification_date = models.DateField(_("Next Verification Date"), null=True, blank=True)
    
    STATUS_CHOICES = [
        ('active', _("Active")),
        ('inactive', _("Inactive")),
        ('under_repair', _("Under Repair")),
        ('decommissioned', _("Decommissioned")),
    ]
    status = models.CharField(_("Status"), max_length=20, choices=STATUS_CHOICES, default='active')

    additional_info = models.TextField(_("Additional Info"), blank=True)
    notes = models.TextField(_("Notes"), blank=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['inventory_number']),
            models.Index(fields=['status']),
        ]
        verbose_name = _("Equipment")
        verbose_name_plural = _("Equipment")

    def __str__(self):
        return f"{self.name} ({self.inventory_number})"

class EquipmentRegistry(models.Model):
    equipment = models.ForeignKey('Equipment', on_delete=models.CASCADE)
    authorized_since = models.DateField(null=True, blank=True) 
    authorized_user = models.ForeignKey(Employee, on_delete=models.CASCADE)
    authorized_from = models.DateField(null=True, blank=True)
    authorized_until = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('maintenance', 'Maintenance'),
    ], default='active')
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Equipment Registry Entry"
        verbose_name_plural = "Equipment Registry"
        unique_together = ('equipment', 'authorized_user')

    def __str__(self):
        return f"{self.equipment} - {self.authorized_user}"


class MaintenanceRecord(models.Model):
    MAINTENANCE_TYPE_CHOICES = [
        ('routine', _('Routine Maintenance')),
        ('repair', _('Repair')),
        ('calibration', _('Calibration')),
        ('inspection', _('Inspection')),
        ('upgrade', _('Upgrade/Modification')),
        ('other', _('Other')),
    ]
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE, related_name='maintenance_records', verbose_name=_('Equipment'))
    maintenance_date = models.DateField(_('Maintenance Date'), default=timezone.now)
    maintenance_type = models.CharField(_('Maintenance Type'), max_length=20, choices=MAINTENANCE_TYPE_CHOICES, default='routine')
    performed_by = models.CharField(_('Performed By'), max_length=255)
    description = models.TextField(_('Description'))
    next_maintenance_date = models.DateField(_('Next Maintenance Date'), blank=True, null=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    def __str__(self):
        return f"{self.get_maintenance_type_display()} on {self.maintenance_date}"

    class Meta:
        verbose_name = _('Maintenance Record')
        verbose_name_plural = _('Maintenance Records')
        ordering = ['-maintenance_date']
        indexes = [
            models.Index(fields=['maintenance_date'], name='maint_date_idx'),
            models.Index(fields=['equipment'], name='maint_equip_idx'),
            models.Index(fields=['next_maintenance_date'], name='next_maint_idx'),
        ]


class EquipmentDocument(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    title = models.CharField(_("Title"), max_length=255)  # ← ŠIS JĀPIEVIENO
    document = models.FileField(upload_to='equipment_documents/')
    external_url = models.URLField(blank=True, null=True)
    document_type = models.CharField(max_length=100, blank=True, null=True)
    internal_reference = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='equipment_documents_uploaded',
        verbose_name=_('Uploaded by')
    )

    class Meta:
        verbose_name = _('Equipment Document')
        verbose_name_plural = _('Equipment Documents')
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['equipment'], name='doc_equipment_idx'),
            models.Index(fields=['title'], name='doc_title_idx'),
        ]

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = _('Equipment Document')
        verbose_name_plural = _('Equipment Documents')
        ordering = ['-uploaded_at']
        indexes = [
            models.Index(fields=['equipment'], name='doc_equipment_idx'),
            models.Index(fields=['title'], name='doc_title_idx'),
        ]
