from django.db import models
from django.utils.translation import gettext_lazy as _


class Position(models.Model):
    """Model representing a job position within a department."""
    title = models.CharField(_("Title"), max_length=100)
    department = models.ForeignKey(
        'company.Department',
        on_delete=models.CASCADE,
        related_name='positions',
        verbose_name=_("Department")
    )
    description = models.TextField(_("Description"), blank=True)
    requirements = models.TextField(_("Requirements"), blank=True)
    salary_range = models.CharField(_("Salary Range"), max_length=100, blank=True)
    level = models.CharField(_("Level"), max_length=50, blank=True)
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        verbose_name = _("Position")
        verbose_name_plural = _("Positions")
        ordering = ['department', 'title']

    def __str__(self):
        return f"{self.title} ({self.department})"
