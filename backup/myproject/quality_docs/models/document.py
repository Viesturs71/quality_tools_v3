"""
Quality Document model for managing company documentation.
"""

from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.exceptions import ValidationError

from .document_type import DocumentType


class QualityDocument(models.Model):
    """
    Model representing a quality document in the system.
    Handles document lifecycle, versioning, and approval workflows.
    """
    
    DOCUMENT_STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived'),
        ('superseded', 'Superseded'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    # Basic Information
    title = models.CharField(
        max_length=255,
        help_text='Document title'
    )
    
    document_number = models.CharField(
        max_length=50,
        unique=True,
        help_text='Unique document identifier'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Document description and purpose'
    )
    
    # Document Type and Section
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.CASCADE,
        related_name='documents',
        help_text='Type of document'
    )
    
    section = models.ForeignKey(
        'DocumentSection',
        on_delete=models.CASCADE,
        related_name='documents',
        help_text='Document section classification'
    )
    
    # Status and Workflow
    status = models.CharField(
        max_length=20,
        choices=DOCUMENT_STATUS_CHOICES,
        default='draft',
        help_text='Current document status'
    )
    
    priority = models.CharField(
        max_length=10,
        choices=PRIORITY_CHOICES,
        default='medium',
        help_text='Document priority level'
    )
    
    # Version Control
    version = models.CharField(
        max_length=20,
        default='1.0',
        help_text='Document version number'
    )
    
    previous_version = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='newer_versions',
        help_text='Previous version of this document'
    )
    
    # People and Responsibilities
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='authored_documents',
        help_text='Document author'
    )
    
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='owned_documents',
        help_text='Document owner responsible for maintenance'
    )
    
    reviewers = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='DocumentReview',
        related_name='reviewing_documents',
        blank=True,
        help_text='Users assigned to review this document'
    )
    
    approver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='approved_documents',
        help_text='User who approved this document'
    )
    
    # Content and Files
    content = models.TextField(
        blank=True,
        help_text='Document content in markdown or rich text format'
    )
    
    file = models.FileField(
        upload_to='quality_docs/documents/%Y/%m/',
        null=True,
        blank=True,
        help_text='Document file attachment'
    )
    
    # Dates
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    approved_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date when document was approved'
    )
    
    published_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date when document was published'
    )
    
    review_due_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date when document review is due'
    )
    
    next_review_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Next scheduled review date'
    )
    
    # Metadata
    tags = models.CharField(
        max_length=255,
        blank=True,
        help_text='Comma-separated tags for categorization'
    )
    
    is_template = models.BooleanField(
        default=False,
        help_text='Whether this document serves as a template'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this document is currently active'
    )
    
    class Meta:
        db_table = 'quality_docs_document'
        verbose_name = 'Quality Document'
        verbose_name_plural = 'Quality Documents'
        ordering = ['-updated_at', 'document_number']
        indexes = [
            models.Index(fields=['document_number']),
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['document_type', 'section']),
            models.Index(fields=['author', 'created_at']),
        ]
    
    def __str__(self):
        return f"{self.document_number} - {self.title}"
    
    def clean(self):
        """Validate the document."""
        if self.status == 'approved' and not self.approver:
            raise ValidationError('Approved documents must have an approver.')
        
        if self.previous_version and self.previous_version.pk == self.pk:
            raise ValidationError('Document cannot be its own previous version.')
    
    def save(self, *args, **kwargs):
        self.full_clean()
        
        # Set approved_date when status changes to approved
        if self.status == 'approved' and not self.approved_date:
            self.approved_date = timezone.now()
        
        # Set published_date when status changes to published
        if self.status == 'published' and not self.published_date:
            self.published_date = timezone.now()
        
        super().save(*args, **kwargs)
    
    @property
    def full_document_number(self):
        """Return formatted document number with version."""
        return f"{self.document_number} v{self.version}"
    
    @property
    def is_overdue_for_review(self):
        """Check if document is overdue for review."""
        if not self.next_review_date:
            return False
        return timezone.now().date() > self.next_review_date.date()
    
    @property
    def pending_reviews(self):
        """Get pending reviews for this document."""
        return self.reviews.filter(status='pending')
    
    @property
    def completed_reviews(self):
        """Get completed reviews for this document."""
        return self.reviews.filter(status__in=['approved', 'rejected'])
    
    def can_user_edit(self, user):
        """Check if user can edit this document."""
        if user == self.author or user == self.owner:
            return True
        return user.has_perm('quality_docs.change_qualitydocument')
    
    def can_user_approve(self, user):
        """Check if user can approve this document."""
        return user == self.approver or user.has_perm('quality_docs.approve_qualitydocument')
