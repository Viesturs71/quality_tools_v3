from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.company.models import Department


class Employee(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='personnel_profile', null=True, blank=True
    )
    employee_id = models.CharField(max_length=50, unique=True, verbose_name=_("Employee ID"))
    first_name = models.CharField(max_length=100, verbose_name=_("First Name"))
    last_name = models.CharField(max_length=100, verbose_name=_("Last Name"))
    position = models.CharField(max_length=100, verbose_name=_("Position"))
    department = models.ForeignKey(
        Department, on_delete=models.SET_NULL, null=True, blank=True,
        related_name='personnel_employees',  # Changed from 'employees' to 'personnel_employees'
        verbose_name=_("Department")
    )
    email = models.EmailField(verbose_name=_("Email"), blank=True)
    phone = models.CharField(max_length=20, blank=True, verbose_name=_("Phone"))
    hire_date = models.DateField(null=True, blank=True, verbose_name=_("Hire Date"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    notes = models.TextField(blank=True, verbose_name=_("Notes"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Employee")
        verbose_name_plural = _("Employees")
        ordering = ['last_name', 'first_name']

    def __str__(self):
        return f"{self.last_name}, {self.first_name} ({self.employee_id})"
