from django.db import models
from django.utils.translation import gettext_lazy as _
from .employee import Employee


class Education(models.Model):
    EDUCATION_LEVELS = [
        ('HIGH_SCHOOL', _('High School')),
        ('VOCATIONAL', _('Vocational School')),
        ('BACHELOR', _('Bachelor\'s Degree')),
        ('MASTER', _('Master\'s Degree')),
        ('DOCTORATE', _('Doctorate')),
        ('OTHER', _('Other')),
    ]

    employee = models.ForeignKey(
        Employee, on_delete=models.CASCADE,
        related_name='education', verbose_name=_("Employee")
    )
    institution = models.CharField(max_length=255, verbose_name=_("Educational Institution"))
    level = models.CharField(max_length=20, choices=EDUCATION_LEVELS, verbose_name=_("Education Level"))
    field_of_study = models.CharField(max_length=255, blank=True, verbose_name=_("Field of Study"))
    degree = models.CharField(max_length=255, blank=True, verbose_name=_("Degree"))
    start_date = models.DateField(verbose_name=_("Start Date"))
    end_date = models.DateField(null=True, blank=True, verbose_name=_("End Date"))
    is_completed = models.BooleanField(default=True, verbose_name=_("Completed"))
    description = models.TextField(blank=True, verbose_name=_("Description"))
    document = models.FileField(upload_to='education_documents/', null=True, blank=True, verbose_name=_("Diploma/Certificate"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Education")
        ordering = ['-end_date', '-start_date']

    def __str__(self):
        return f"{self.employee} - {self.degree} ({self.institution})"
