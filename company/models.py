from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Company(models.Model):
    """Model for companies in the system"""
    name = models.CharField(_('Company Name'), max_length=255)
    code = models.CharField(_('Company Code'), max_length=50, unique=True)
    address = models.TextField(_('Address'), blank=True)
    contact_email = models.EmailField(_('Contact Email'), blank=True)
    contact_phone = models.CharField(_('Contact Phone'), max_length=50, blank=True)
    website = models.URLField(_('Website'), blank=True)
    active = models.BooleanField(_('Active'), default=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Company')
        verbose_name_plural = _('Companies')
        ordering = ['name']

    def __str__(self):
        return self.name

class Department(models.Model):
    """Model for departments within companies"""
    company = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        related_name='departments',
        verbose_name=_('Company')
    )
    name = models.CharField(_('Department Name'), max_length=255)
    code = models.CharField(_('Department Code'), max_length=50)
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name=_('Parent Department')
    )
    description = models.TextField(_('Description'), blank=True)
    manager = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # Use settings.AUTH_USER_MODEL instead of 'auth.User'
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='managed_departments',
        verbose_name=_('Department Manager')
    )
    active = models.BooleanField(_('Active'), default=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['company', 'name']
        unique_together = [['company', 'code']]

    def __str__(self):
        return f"{self.name} ({self.company.name})"
