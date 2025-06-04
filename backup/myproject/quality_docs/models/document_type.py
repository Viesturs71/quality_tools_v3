"""
Document Type model for managing different types of quality documents.
"""

from django.db import models
from django.core.exceptions import ValidationError


class DocumentType(models.Model):
    """
    Model representing different types of quality documents.
    Used to categorize documents like Work Instructions, Procedures, Forms, etc.
    """
    
    name = models.CharField(
        max_length=100,
        unique=True,
        help_text='Document type name (e.g., Work Instructions, Procedures, Forms)'
    )
    
    abbreviation = models.CharField(
        max_length=10,
        unique=True,
        help_text='Short abbreviation for the document type (e.g., WI, PROC, FORM)'
    )
    
    description = models.TextField(
        help_text='Explanation of document purpose and development requirements'
    )
    
    color_code = models.CharField(
        max_length=7,
        default='#2563eb',
        help_text='Hex color code for visual identification'
    )
    
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='Icon name from Heroicons for visual representation'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this document type is currently active'
    )
    
    requires_approval = models.BooleanField(
        default=True,
        help_text='Whether documents of this type require approval workflow'
    )
    
    retention_period = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text='Document retention period in years'
    )
    
    sort_order = models.PositiveIntegerField(
        default=0,
        help_text='Sort order for display purposes'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quality_docs_document_type'
        verbose_name = 'Document Type'
        verbose_name_plural = 'Document Types'
        ordering = ['sort_order', 'name']
        indexes = [
            models.Index(fields=['is_active', 'sort_order']),
            models.Index(fields=['abbreviation']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.abbreviation})"
    
    def clean(self):
        """Validate the document type."""
        if self.abbreviation:
            self.abbreviation = self.abbreviation.upper()
        
        if self.color_code and not self.color_code.startswith('#'):
            self.color_code = f"#{self.color_code}"
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def document_count(self):
        """Get the number of documents of this type."""
        return self.documents.filter(is_active=True).count()
    
    @property
    def pending_approval_count(self):
        """Get the number of documents pending approval for this type."""
        return self.documents.filter(status='review', is_active=True).count()
