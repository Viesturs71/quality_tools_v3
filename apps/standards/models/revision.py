from django.db import models
from django.utils.translation import gettext_lazy as _


class StandardRevision(models.Model):
    standard = models.ForeignKey(
        'standards.Standard',  # Corrected string reference
        on_delete=models.CASCADE,
        related_name='revisions',
        verbose_name=_('Standard')
    )
    revision_number = models.CharField(_('Revision Number'), max_length=50)
    effective_date = models.DateField(_('Effective Date'))
    notes = models.TextField(_('Notes'), blank=True, null=True)

    class Meta:
        verbose_name = _('Standard Revision')
        verbose_name_plural = _('Standard Revisions')
        ordering = ['-effective_date']

    def __str__(self):
        return f"{self.standard} - Rev {self.revision_number}"
