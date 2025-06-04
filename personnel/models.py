# personnel/models.py
from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _
from simple_history.models import HistoricalRecords

from company.models import Company

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    modules = models.JSONField(default=list)

    def __str__(self):
        return self.user.username

class Department(models.Model):
    name = models.CharField(_('Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='personnel_departments'  # Changed from 'departments' to 'personnel_departments'
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField(_('Position Name'), max_length=100)
    description = models.TextField(_('Description'), blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')

    def __str__(self):
        return self.name

class Field(models.Model):
    name = models.CharField(_('Field Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Field')
        verbose_name_plural = _('Fields')

    def __str__(self):
        return self.name

class Education(models.Model):
    name = models.CharField(_('Name'), max_length=255)
    description = models.TextField(_('Description'), blank=True, null=True)
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Education')
        verbose_name_plural = _('Education')

    def __str__(self):
        return self.name

class Employee(models.Model):
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    email = models.EmailField(_('Email'), unique=True)
    hire_date = models.DateField(_('Hire Date'), blank=True, null=True)
    department = models.ForeignKey(
        Department,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='employees'
    )
    position = models.ForeignKey(
        Position,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    history = HistoricalRecords()

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
