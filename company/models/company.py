from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

class Company(models.Model):
    """Model representing a company."""
    name = models.CharField(_('name'), max_length=255)
    identifier = models.CharField(_('identifier'), max_length=50, unique=True)
    code = models.CharField(_('code'), max_length=50, blank=True, null=True)  # Added missing field
    registration_number = models.CharField(_('registration number'), max_length=50, blank=True, null=True)  # Added missing field
    address = models.TextField(_('address'), blank=True, null=True)
    phone = models.CharField(_('phone'), max_length=20, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    website = models.URLField(_('website'), blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    is_active = models.BooleanField(_('is active'), default=True)  # Added this field
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        app_label = 'company'
        verbose_name = _("Company")
        verbose_name_plural = _("Companies")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Department(models.Model):
    name = models.CharField(_('name'), max_length=255)
    code = models.CharField(_('code'), max_length=50, blank=True, null=True)
    description = models.TextField(_('description'), blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='departments', verbose_name=_('company'))
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        app_label = 'company'
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
        ordering = ["name"]

    def __str__(self):
        return self.name


class Location(models.Model):
    name = models.CharField(_('name'), max_length=255)
    address = models.TextField(_('address'), blank=True, null=True)
    city = models.CharField(_('city'), max_length=100, blank=True, null=True)
    postal_code = models.CharField(_('postal code'), max_length=20, blank=True, null=True)
    country = models.CharField(_('country'), max_length=100, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='locations', verbose_name=_('company'))
    is_active = models.BooleanField(_('is active'), default=True)
    created_at = models.DateTimeField(_('created at'), auto_now_add=True)
    updated_at = models.DateTimeField(_('updated at'), auto_now=True)

    class Meta:
        app_label = 'company'
        verbose_name = _("Location")
        verbose_name_plural = _("Locations")
        ordering = ["name"]  # Changed from "user__username" to "name"

    def __str__(self):
        return self.name
