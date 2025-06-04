from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class Department(models.Model):
    """
    Model representing a department or structural unit within the organization.
    Departments are used to organize equipment and assign responsibilities.
    """
    name = models.CharField(_('Department Name'), max_length=100)
    manager_name = models.CharField(_('Manager Name'), max_length=100, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True, null=True)

    # Timestamps
    created_at = models.DateTimeField(_('Created At'), default=timezone.now, editable=False)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name']
        db_table = 'equipment_department'  # Explicitly set the table name

    def __str__(self):
        return self.name
