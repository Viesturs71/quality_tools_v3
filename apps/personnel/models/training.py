from django.db import models
from django.utils.translation import gettext_lazy as _
from .employee import Employee


class Training(models.Model):
    TRAINING_STATUS_CHOICES = [
        ('PLANNED', _('Planned')),
        ('IN_PROGRESS', _('In Progress')),
        ('COMPLETED', _('Completed')),
        ('CANCELLED', _('Cancelled')),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='training_records', verbose_name=_("Employee")
    )
    training_name = models.CharField(max_length=255, verbose_name=_("Training Name"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"))
    status = models.CharField(
        max_length=20, choices=TRAINING_STATUS_CHOICES, default='PLANNED', verbose_name=_("Status")
    )
    provider = models.CharField(max_length=255, blank=True, verbose_name=_("Training Provider"))
    certificate_issued = models.BooleanField(default=False, verbose_name=_("Certificate Issued"))
    certificate_number = models.CharField(max_length=100, blank=True, verbose_name=_("Certificate Number"))
    certificate_date = models.DateField(null=True, blank=True, verbose_name=_("Certificate Date"))
    certificate_document = models.FileField(
        upload_to='training_certificates/', null=True, blank=True, verbose_name=_("Certificate Document")
    )
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Training")
        verbose_name_plural = _("Training Records")
        ordering = ['-start_date']

    def __str__(self):
        return f"{self.employee} - {self.training_name}"
