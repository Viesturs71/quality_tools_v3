# apps/standards/models/standard.py

from django.db import models
from django.utils.translation import gettext_lazy as _

# import the one-and-only StandardCategory (keep this file in standard_category.py)
from .standard_category import StandardCategory


class Standard(models.Model):
    category = models.ForeignKey(
        StandardCategory,
        on_delete=models.CASCADE,
        related_name='standards',
        verbose_name=_('Category'),
    )
    code        = models.CharField(_('Standard Code'), max_length=20, unique=True)
    title       = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)

    class Meta:
        verbose_name        = _('Standard')
        verbose_name_plural = _('Standards')
        ordering            = ('category__code', 'code')

    def __str__(self):
        return f"{self.code} – {self.title}"
