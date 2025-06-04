"""
Admin configuration for quality_docs app.
"""
from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Import models
from quality_docs.models import (
    QualityDocument, DocumentType, DocumentCategory, DocumentSection,
    DocumentAttachment, DocumentReview, ApprovalFlow, ApprovalStep,
    SignatureRequest, DocumentDistribution, DocumentAcknowledgment
)

# Register models with detailed admin classes
@admin.register(QualityDocument)
class QualityDocumentAdmin(admin.ModelAdmin):
    list_display = ['document_number', 'title', 'document_type', 'get_status', 'is_approved']
    list_filter = ['status', 'document_type', 'is_approved']  # Removed 'company' field
    search_fields = ['title', 'document_number']  # Removed company_name from search fields
    readonly_fields = ['uploaded_at', 'uploaded_by', 'get_document_info']
    
    def get_status(self, obj):
        return obj.get_status_display()
    get_status.short_description = 'Status'
    
    def get_document_info(self, obj):
        """Method to display document info in admin"""
        return f"Created: {obj.created_at}, Last Updated: {obj.updated_at}"
    get_document_info.short_description = 'Document Information'

# Define the DocumentTypeAdmin class
class DocumentTypeAdmin(admin.ModelAdmin):
    """Admin interface for DocumentType model."""
    list_display = ('name', 'abbreviation')
    search_fields = ('name', 'abbreviation', 'description')

# Register other models with their admin classes
@admin.register(DocumentCategory)
class DocumentCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(DocumentSection)
class DocumentSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'identifier', 'parent')
    list_filter = ('parent',)
    search_fields = ('name', 'identifier')

# Register remaining models
admin.site.register(DocumentAttachment)
admin.site.register(DocumentReview)
admin.site.register(ApprovalFlow)
admin.site.register(ApprovalStep)
admin.site.register(SignatureRequest)
admin.site.register(DocumentDistribution)
admin.site.register(DocumentAcknowledgment)

# Admin site customization
admin.site.site_header = _("Quality Tools Administration")
admin.site.site_title = _("Quality Tools Admin")
admin.site.index_title = _("Welcome to Quality Tools Administration")
