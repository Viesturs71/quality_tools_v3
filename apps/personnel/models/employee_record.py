from django.db import models
from django.utils.translation import gettext_lazy as _
from .employee import Employee


class EmployeeRecord(models.Model):
    RECORD_TYPES = [
        ('CONTRACT', _('Employment Contract')),
        ('AGREEMENT', _('Agreement')),
        ('ASSESSMENT', _('Performance Assessment')),
        ('DISCIPLINARY', _('Disciplinary Action')),
        ('AWARD', _('Award or Recognition')),
        ('OTHER', _('Other Document')),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='employee_records', verbose_name=_("Employee")
    )
    record_type = models.CharField(max_length=20, choices=RECORD_TYPES, verbose_name=_("Record Type"))
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    issue_date = models.DateField(verbose_name=_("Issue Date"))
    expiry_date = models.DateField(null=True, blank=True, verbose_name=_("Expiry Date"))
    document = models.FileField(upload_to='employee_records/', null=True, blank=True, verbose_name=_("Document"))
    is_confidential = models.BooleanField(default=False, verbose_name=_("Confidential"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Employee Record")
        verbose_name_plural = _("Employee Records")
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.employee} - {self.get_record_type_display()}: {self.title}"
