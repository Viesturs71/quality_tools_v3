from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model

User = get_user_model()


class Document(models.Model):
    """Base document model for the document management system."""
    title = models.CharField(_('Title'), max_length=255)
    document_number = models.CharField(_('Document Number'), max_length=50, unique=True, blank=True)
    version = models.CharField(_('Version'), max_length=20, default='1.0')
    description = models.TextField(_('Description'), blank=True)
    content = models.TextField(_('Content'), blank=True)
    
    # Document status choices
    STATUS_DRAFT = 'draft'
    STATUS_REVIEW = 'review'
    STATUS_APPROVED = 'approved'
    STATUS_PUBLISHED = 'published'
    STATUS_ARCHIVED = 'archived'
    
    STATUS_CHOICES = [
        (STATUS_DRAFT, _('Draft')),
        (STATUS_REVIEW, _('In Review')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_PUBLISHED, _('Published')),
        (STATUS_ARCHIVED, _('Archived')),
    ]
    
    status = models.CharField(
        _('Status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT
    )
    
    # Document type choices
    TYPE_PROCEDURE = 'procedure'
    TYPE_INSTRUCTION = 'instruction'
    TYPE_FORM = 'form'
    TYPE_TEMPLATE = 'template'
    TYPE_RECORD = 'record'
    TYPE_REPORT = 'report'
    TYPE_POLICY = 'policy'
    
    TYPE_CHOICES = [
        (TYPE_PROCEDURE, _('Procedure')),
        (TYPE_INSTRUCTION, _('Work Instruction')),
        (TYPE_FORM, _('Form')),
        (TYPE_TEMPLATE, _('Template')),
        (TYPE_RECORD, _('Record')),
        (TYPE_REPORT, _('Report')),
        (TYPE_POLICY, _('Policy')),
    ]
    
    document_type = models.CharField(
        _('Document Type'),
        max_length=20,
        choices=TYPE_CHOICES,
        default=TYPE_PROCEDURE
    )
    
    # Metadata
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_documents',
        verbose_name=_('Created By')
    )
    updated_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='updated_documents',
        verbose_name=_('Updated By')
    )
    approved_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='approved_documents',
        verbose_name=_('Approved By')
    )
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    approved_at = models.DateTimeField(_('Approved At'), null=True, blank=True)
    published_at = models.DateTimeField(_('Published At'), null=True, blank=True)
    
    # Relationships (can be customized per project needs)
    parent_document = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='child_documents',
        verbose_name=_('Parent Document')
    )
    
    class Meta:
        verbose_name = _('Document')
        verbose_name_plural = _('Documents')
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.document_number} - {self.title} (v{self.version})"
    
    def get_status_display_class(self):
        """Return a CSS class based on document status for UI styling."""
        status_classes = {
            self.STATUS_DRAFT: 'text-secondary',
            self.STATUS_REVIEW: 'text-primary',
            self.STATUS_APPROVED: 'text-success',
            self.STATUS_PUBLISHED: 'text-info',
            self.STATUS_ARCHIVED: 'text-muted',
        }
        return status_classes.get(self.status, '')
