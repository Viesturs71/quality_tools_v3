"""
Document Section model for hierarchical organization of quality documents.
"""

from django.db import models
from django.core.exceptions import ValidationError


class DocumentSection(models.Model):
    """
    Model representing hierarchical sections for document organization.
    Similar to file nomenclature with sections, subsections, and sub-subsections.
    """
    
    identifier = models.CharField(
        max_length=20,
        unique=True,
        help_text='Section identifier (e.g., 1, 1.1, 1.1.1, A, A.1)'
    )
    
    name = models.CharField(
        max_length=100,
        help_text='Section name'
    )
    
    title = models.CharField(
        max_length=200,
        help_text='Full section title'
    )
    
    description = models.TextField(
        blank=True,
        help_text='Description of what documents belong in this section'
    )
    
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='subsections',
        help_text='Parent section for hierarchical structure'
    )
    
    level = models.PositiveIntegerField(
        default=1,
        help_text='Hierarchy level (1=main section, 2=subsection, 3=sub-subsection)'
    )
    
    sort_order = models.PositiveIntegerField(
        default=0,
        help_text='Sort order within the same level'
    )
    
    is_active = models.BooleanField(
        default=True,
        help_text='Whether this section is currently active'
    )
    
    color_code = models.CharField(
        max_length=7,
        default='#6366f1',
        help_text='Hex color code for visual identification'
    )
    
    icon = models.CharField(
        max_length=50,
        blank=True,
        help_text='Icon name from Heroicons for visual representation'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'quality_docs_document_section'
        verbose_name = 'Document Section'
        verbose_name_plural = 'Document Sections'
        ordering = ['level', 'sort_order', 'identifier']
        indexes = [
            models.Index(fields=['parent', 'level']),
            models.Index(fields=['is_active', 'level']),
            models.Index(fields=['identifier']),
        ]
    
    def __str__(self):
        return f"{self.identifier} - {self.title}"
    
    def clean(self):
        """Validate the document section."""
        if self.parent:
            # Check for circular references
            if self.parent == self:
                raise ValidationError('Section cannot be its own parent.')
            
            # Set level based on parent
            self.level = self.parent.level + 1
            
            # Validate maximum nesting level
            if self.level > 4:
                raise ValidationError('Maximum nesting level is 4.')
        else:
            self.level = 1
    
    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    
    @property
    def full_path(self):
        """Get the full hierarchical path."""
        if self.parent:
            return f"{self.parent.full_path} > {self.title}"
        return self.title
    
    @property
    def document_count(self):
        """Get the number of documents in this section."""
        return self.documents.filter(is_active=True).count()
    
    @property
    def total_document_count(self):
        """Get the total number of documents in this section and all subsections."""
        count = self.document_count
        for subsection in self.subsections.filter(is_active=True):
            count += subsection.total_document_count
        return count
    
    @property
    def has_subsections(self):
        """Check if this section has active subsections."""
        return self.subsections.filter(is_active=True).exists()
    
    def get_all_subsections(self):
        """Get all subsections recursively."""
        subsections = []
        for subsection in self.subsections.filter(is_active=True):
            subsections.append(subsection)
            subsections.extend(subsection.get_all_subsections())
        return subsections
    
    def get_root_section(self):
        """Get the root section of this hierarchy."""
        if self.parent:
            return self.parent.get_root_section()
        return self
