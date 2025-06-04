"""
Document Review model for managing document review processes.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class DocumentReview(models.Model):
    """
    Model representing a document review process.
    Tracks reviewers assigned to documents and their review status.
    """
    
    REVIEW_STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('in_progress', 'In Progress'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('revision_required', 'Revision Required'),
    ]
    
    document = models.ForeignKey(
        'QualityDocument',
        on_delete=models.CASCADE,
        related_name='reviews',
        help_text='Document being reviewed'
    )
    
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='document_reviews',
        help_text='User assigned to review the document'
    )
    
    status = models.CharField(
        max_length=20,
        choices=REVIEW_STATUS_CHOICES,
        default='pending',
        help_text='Current status of the review'
    )
    
    assigned_date = models.DateTimeField(
        default=timezone.now,
        help_text='Date when the review was assigned'
    )
    
    review_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text='Date when the review was completed'
    )
    
    comments = models.TextField(
        blank=True,
        help_text='Review comments and feedback'
    )
    
    review_order = models.PositiveIntegerField(
        default=1,
        help_text='Order in which this review should be completed'
    )
    
    is_required = models.BooleanField(
        default=True,
        help_text='Whether this review is required for document approval'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quality_docs_document_review'
        verbose_name = 'Document Review'
        verbose_name_plural = 'Document Reviews'
        unique_together = ['document', 'reviewer']
        ordering = ['review_order', 'assigned_date']
        indexes = [
            models.Index(fields=['document', 'status']),
            models.Index(fields=['reviewer', 'status']),
            models.Index(fields=['assigned_date']),
        ]
    
    def __str__(self):
        return f"Review of {self.document.title} by {self.reviewer.get_full_name() or self.reviewer.username}"
    
    def save(self, *args, **kwargs):
        if self.status in ['approved', 'rejected'] and not self.review_date:
            self.review_date = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def is_completed(self):
        """Check if the review is completed."""
        return self.status in ['approved', 'rejected']
    
    @property
    def days_pending(self):
        """Calculate number of days the review has been pending."""
        if self.is_completed:
            return 0
        return (timezone.now() - self.assigned_date).days
