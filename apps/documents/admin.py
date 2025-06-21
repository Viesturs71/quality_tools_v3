from django.contrib import admin
from .models import (
    QualityDocument,
    DocumentSection,
    DocumentAttachment,
    DocumentRevision,
)
from .models.document import Document


@admin.register(QualityDocument)
class QualityDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_number', 'version', 'created_at')
    search_fields = ('title', 'document_number')


@admin.register(DocumentSection)
class DocumentSectionAdmin(admin.ModelAdmin):
    list_display = ('section_number', 'title', 'created_at')
    search_fields = ('section_number', 'title')


@admin.register(DocumentAttachment)
class DocumentAttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)


@admin.register(DocumentRevision)
class DocumentRevisionAdmin(admin.ModelAdmin):
    list_display = ('revision_number', 'revision_date', 'is_current')
    search_fields = ('revision_number',)


@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'uploaded_by', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('created_at', 'uploaded_by')
