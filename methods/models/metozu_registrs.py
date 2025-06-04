# quality_docs/models/metozu_registrs.py
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class MetozuRegistrs(models.Model):
    name = models.CharField(
        max_length=255,
        verbose_name=_('Metodes nosaukums')
    )
    identification = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Metodes identifikācija')
    )
    investigation_field = models.CharField(
        max_length=255,
        verbose_name=_('Izmeklējumu joma'),
        null=True,
        blank=True
    )
    analyzer = models.CharField(
        max_length=255,
        verbose_name=_('Analizātors/iekārta'),
        null=True,
        blank=True
    )
    technology = models.TextField(
        verbose_name=_('Izmeklējumu tehnoloģija'),
        null=True,
        blank=True
    )
    test_material = models.CharField(
        max_length=255,
        verbose_name=_('Izmeklējamais materiāls'),
        null=True,
        blank=True
    )
    verification_date = models.DateField(
        verbose_name=_('Verifikācijas datums'),
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=255,
        verbose_name=_('Atrašanās vieta'),
        null=True,
        blank=True
    )

    document = models.FileField(
        upload_to='method_documents/',
        verbose_name=_('Metodes dokuments'),
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Izveidoja'),
        related_name='created_methods'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Izveidots')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Atjaunināts')
    )

    class Meta:
        app_label = 'methods'
        verbose_name = _('Metode')
        verbose_name_plural = _('Metodes')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.identification})"
