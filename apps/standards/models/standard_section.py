from django.db import models
from django.utils.translation import gettext_lazy as _

class StandardSection(models.Model):
    standard = models.ForeignKey(
        'standards.Standard',
        on_delete=models.CASCADE,
        related_name='sections',
        verbose_name=_('Standard')
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='subsections',
        verbose_name=_('Parent Section')
    )
    code = models.CharField(_('Code'), max_length=50)
    title = models.CharField(_('Section title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['standard', 'code', 'order']
        verbose_name = _('Standard Section')
        verbose_name_plural = _('Standard Sections')
        unique_together = ['standard', 'code']

    def __str__(self):
        return f"{self.code} - {self.title}"
        
    def get_full_code(self):
        """Return the full hierarchical code of this section."""
        if self.parent:
            return f"{self.parent.get_full_code()}.{self.code}"
        return self.code
