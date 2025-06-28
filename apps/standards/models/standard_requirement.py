"""
StandardRequirement model definition for standards app.
"""
from django.db import models
from django.utils.translation import gettext_lazy as _


class StandardRequirement(models.Model):
    """
    Represents a specific requirement within a standard section.
    """
    section = models.ForeignKey(
        'standards.StandardSection',
        on_delete=models.CASCADE,
        related_name='requirements',
        verbose_name=_('Section')
    )
    code = models.CharField(_('Code'), max_length=20)
    # Multilingual fields (required)
    text_original = models.TextField(_('Requirement Text (original)'))
    text_alt = models.TextField(_('Requirement Text (alternative)'))
    description_original = models.TextField(_('Description (original)'))
    description_alt = models.TextField(_('Description (alternative)'))
    is_mandatory = models.BooleanField(_('Is Mandatory'), default=True)
    order = models.PositiveIntegerField(_('Display Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Standard Requirement')
        verbose_name_plural = _('Standard Requirements')
        ordering = ['section', 'order', 'code']
        unique_together = ('section', 'code')

    def __str__(self):
        return f"{self.section.code}.{self.code} - {self.text_original[:50]}"

    @property
    def standard(self):
        """
        Returns the standard this requirement belongs to.
        """
        return self.section.standard

    def get_text(self, use_alt=False):
        return self.text_alt if use_alt else self.text_original

    def get_description(self, use_alt=False):
        return self.description_alt if use_alt else self.description_original
