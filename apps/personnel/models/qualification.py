from django.db import models
from django.utils.translation import gettext_lazy as _
from .employee import Employee


class Qualification(models.Model):
    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='qualifications', verbose_name=_("Employee")
    )
    qualification_type = models.CharField(max_length=100, verbose_name=_("Qualification Type"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    issue_date = models.DateField(verbose_name=_("Issue Date"))
    expiry_date = models.DateField(null=True, blank=True, verbose_name=_("Expiry Date"))
    issuing_organization = models.CharField(max_length=255, blank=True, verbose_name=_("Issuing Organization"))
    certificate_number = models.CharField(max_length=100, blank=True, verbose_name=_("Certificate Number"))
    document = models.FileField(upload_to='qualification_documents/', null=True, blank=True, verbose_name=_("Document"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Qualification")
        verbose_name_plural = _("Qualifications")
        ordering = ['-issue_date']

    def __str__(self):
        return f"{self.employee} - {self.qualification_type}"
