from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .category import Category
from apps.documents.utils.document_numbering import (
    generate_document_number,
    validate_document_number_format,
    validate_document_number_uniqueness,
    parse_document_number,
    suggest_next_sequence_number,
)


class QualityDocument(models.Model):
    """Model representing a quality document."""
    title = models.CharField(max_length=255, verbose_name=_("Title"))
    document_number = models.CharField(max_length=50, unique=True, verbose_name=_("Document Number"))
    version = models.CharField(max_length=20, verbose_name=_("Version"))
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_("Created At"))
    updated_at = models.DateTimeField(auto_now=True, verbose_name=_("Updated At"))

    class Meta:
        verbose_name = _("Quality Document")
        verbose_name_plural = _("Quality Documents")
        ordering = ["document_number"]

    def __str__(self):
        return f"{self.document_number}: {self.title}"

class Document(models.Model):
    """Model representing a quality document."""
    DOCUMENT_TYPES = (
        ('policy', 'Politika'),
        ('procedure', 'Procedūra'),
        ('instruction', 'Instrukcija'),
        ('form', 'Veidlapa'),
        ('other', 'Cits'),
    )
    
    STATUS_CHOICES = (
        ('draft', 'Melnraksts'),
        ('review', 'Pārskatīšanā'),
        ('approved', 'Apstiprināts'),
        ('published', 'Publicēts'),
        ('archived', 'Arhivēts'),
    )
    
    title = models.CharField(max_length=200, verbose_name='Nosaukums')
    document_number = models.CharField(max_length=50, unique=True, verbose_name='Dokumenta numurs')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, verbose_name='Dokumenta veids')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft', verbose_name='Statuss')
    content = models.TextField(verbose_name='Saturs')
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_documents', verbose_name='Izveidoja')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Izveidošanas datums')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atjaunināšanas datums')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_documents', verbose_name='Apstiprināja')
    approved_at = models.DateTimeField(null=True, blank=True, verbose_name='Apstiprināšanas datums')
    version = models.CharField(max_length=20, default='1.0', verbose_name='Versija')
    attachment = models.FileField(upload_to='documents/attachments/', null=True, blank=True)  # Add this field
    description = models.TextField(null=True, blank=True)  # Add this field
    uploaded_by = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='document_uploaded_by',  # Unique related_name
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = 'Dokuments'
        verbose_name_plural = 'Dokumenti'
        ordering = ['-updated_at']
    
    def __str__(self):
        return f"{self.document_number} - {self.title}"
    
    def __str__(self):
        return f"{self.document_number} - {self.title}"
