from django.db import models
from django.utils.translation import gettext_lazy as _


class Audit(models.Model):
    STATUS_CHOICES = [
        ('planned', _('Planned')),
        ('in_progress', _('In Progress')),
        ('completed', _('Completed')),
        ('cancelled', _('Cancelled')),
    ]

    title = models.CharField(_('Title'), max_length=200)
    description = models.TextField(_('Description'), blank=True)
    date = models.DateField(_('Audit Date'))
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default='planned'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = _('Audit')
        verbose_name_plural = _('Audits')
        ordering = ['-date']
        app_label = 'audits'

    def __str__(self):
        return self.title
