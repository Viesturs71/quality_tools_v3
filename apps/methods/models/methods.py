# quality_docs/models/metozu_registrs.py
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Method(models.Model):
    """
    Model representing a testing or analysis method.
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('Method Name')
    )
    identification = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Method Identification')
    )
    investigation_field = models.CharField(
        max_length=255,
        verbose_name=_('Investigation Field'),
        null=True,
        blank=True
    )
    analyzer = models.CharField(
        max_length=255,
        verbose_name=_('Analyzer/Equipment'),
        null=True,
        blank=True
    )
    technology = models.TextField(
        verbose_name=_('Investigation Technology'),
        null=True,
        blank=True
    )
    test_material = models.CharField(
        max_length=255,
        verbose_name=_('Test Material'),
        null=True,
        blank=True
    )
    verification_date = models.DateField(
        verbose_name=_('Verification Date'),
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=255,
        verbose_name=_('Location'),
        null=True,
        blank=True
    )
    # Quality Control Status Fields
    internal_qc_required = models.BooleanField(
        verbose_name=_('Internal QC Required'),
        default=True
    )
    external_qc_required = models.BooleanField(
        verbose_name=_('External QC Required'),
        default=True
    )
    verification_required = models.BooleanField(
        verbose_name=_('Verification Required'),
        default=True
    )
    last_internal_qc_date = models.DateField(
        verbose_name=_('Last Internal QC Date'),
        null=True,
        blank=True
    )
    last_external_qc_date = models.DateField(
        verbose_name=_('Last External QC Date'),
        null=True,
        blank=True
    )
    next_verification_date = models.DateField(
        verbose_name=_('Next Verification Date'),
        null=True,
        blank=True
    )

    document = models.FileField(
        upload_to='method_documents/',
        verbose_name=_('Method Document'),
        null=True,
        blank=True
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('Created By'),
        related_name='created_methods'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )

    class Meta:
        app_label = 'methods'
        verbose_name = _('Method')
        verbose_name_plural = _('Methods')
        ordering = ['name']

    def __str__(self):
        return f"{self.name} ({self.identification})"
