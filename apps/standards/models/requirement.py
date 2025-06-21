from django.db import models
from django.utils.translation import gettext_lazy as _


class StandardRequirement(models.Model):
    standard = models.ForeignKey(
        'standards.Standard',
        on_delete=models.CASCADE,
        related_name='requirements',
        verbose_name=_('Standard')
    )
    description = models.TextField(_('Description'))
    is_mandatory = models.BooleanField(_('Is Mandatory'), default=True)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Standard Requirement')
        verbose_name_plural = _('Standard Requirements')
        ordering = ['-created_at']

    def __str__(self):
        return f"Requirement for {self.standard}: {self.description[:50]}"
