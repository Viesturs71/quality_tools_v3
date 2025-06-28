from django.db import models
from django.utils.translation import gettext_lazy as _


class MethodVerification(models.Model):
    """
    Method verification/validation records.
    Documents the process of confirming that a method is fit for its intended use.
    """
    VERIFICATION_TYPE_CHOICES = [
        ('verification', _('Verification')),
        ('validation', _('Validation')),
        ('revalidation', _('Revalidation')),
    ]

    method = models.ForeignKey(
        'Method',
        on_delete=models.CASCADE,
        related_name='verifications',
        verbose_name=_('Method')
    )
    verification_type = models.CharField(
        _('Verification Type'), 
        max_length=20,
        choices=VERIFICATION_TYPE_CHOICES,
        default='verification'
    )
    verification_date = models.DateField(_('Verification Date'))
    performed_by = models.CharField(_('Performed By'), max_length=255)
    
    # Performance characteristics
    precision_data = models.TextField(_('Precision Data'), blank=True)
    accuracy_data = models.TextField(_('Accuracy Data'), blank=True)
    linearity_data = models.TextField(_('Linearity Data'), blank=True)
    detection_limit = models.CharField(_('Detection Limit'), max_length=100, blank=True)
    quantitation_limit = models.CharField(_('Quantitation Limit'), max_length=100, blank=True)
    
    # Results
    acceptance_criteria = models.TextField(_('Acceptance Criteria'))
    results_summary = models.TextField(_('Results Summary'))
    is_approved = models.BooleanField(_('Approved'), default=False)
    approved_by = models.CharField(_('Approved By'), max_length=255, blank=True)
    approval_date = models.DateField(_('Approval Date'), null=True, blank=True)
    
    # Documents
    protocol_document = models.FileField(_('Protocol Document'), upload_to='method_verification/protocols/', blank=True)
    report_document = models.FileField(_('Report Document'), upload_to='method_verification/reports/', blank=True)
    
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Method Verification')
        verbose_name_plural = _('Method Verifications')
        ordering = ['-verification_date']

    def __str__(self):
        return f"{self.method.name} - {self.get_verification_type_display()} ({self.verification_date})"
