from django.db import models

class Equipment(models.Model):
    # General Information
    name = models.CharField(max_length=255)  # Equipment Name
    type = models.CharField(max_length=255)  # Equipment/Measuring Instrument Type
    model = models.CharField(max_length=255, blank=True, null=True)
    manufacturer = models.CharField(max_length=255, blank=True, null=True)
    inventory_number = models.CharField(max_length=255, unique=True)  # Inventory Number
    serial_number = models.CharField(max_length=255, unique=True)  # Serial Number
    location = models.CharField(max_length=255)  # Location

    # Documentation
    user_manual_file = models.FileField(upload_to='equipment_docs/user_manuals/', blank=True, null=True)
    user_manual_url = models.URLField(blank=True, null=True)
    additional_documentation = models.TextField(blank=True, null=True)

    # Department Information
    department = models.CharField(max_length=255, blank=True, null=True)
    person_responsible = models.CharField(max_length=255, blank=True, null=True)

    # Dates and Financial Information
    manufacture_date = models.DateField(blank=True, null=True)
    purchase_date = models.DateField(blank=True, null=True)
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    # Metrological Control
    metrological_control_type = models.CharField(max_length=255, blank=True, null=True)
    metrological_control_institution = models.CharField(max_length=255, blank=True, null=True)
    certificate_number = models.CharField(max_length=255, blank=True, null=True)
    metrological_control_periodicity = models.IntegerField(blank=True, null=True)  # in days
    next_verification_date = models.DateField(blank=True, null=True)

    # Status Information
    technical_status = models.CharField(max_length=255, blank=True, null=True)
    additional_information = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name
