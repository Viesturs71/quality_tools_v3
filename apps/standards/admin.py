# apps/standards/admin.py

from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    StandardCategory,
    Standard,
    StandardSection,
    StandardRequirement,
    StandardAttachment,
    StandardDocument,
    StandardDocumentLink,
    StandardCompliance,
    StandardRevision
)

class StandardCategoryAdmin(admin.ModelAdmin):
    list_display = ('code', 'title')
    search_fields = ('code', 'title')
    ordering = ('code',)

class StandardAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'category')
    list_filter = ('category',)
    search_fields = ('code', 'title')
    ordering = ('code',)

@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'category')
    list_filter = ('category',)
    search_fields = ('code', 'title')
    ordering = ('code',)

@admin.register(StandardSection)
class StandardSectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'title', 'standard', 'parent')
    list_filter = ('standard',)
    search_fields = ('code', 'title')
    ordering = ('standard', 'code')

@admin.register(StandardRequirement)
class StandardRequirementAdmin(admin.ModelAdmin):
    list_display = (
        'code', 'text_original', 'text_alt',
        'description_original', 'description_alt',
        'section', 'is_mandatory', 'order'
    )
    list_filter = ('section__standard', 'is_mandatory')
    search_fields = (
        'code', 'text_original', 'text_alt',
        'description_original', 'description_alt'
    )
    ordering = ('section', 'order', 'code')

@admin.register(StandardAttachment)
class StandardAttachmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'section', 'created_at')
    list_filter = ('section__standard',)
    search_fields = ('title', 'description')
    ordering = ('-created_at',)

@admin.register(StandardDocument)
class StandardDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_number', 'version', 'status', 'uploaded_at')
    list_filter = ('status', 'is_active')
    search_fields = ('title', 'document_number', 'description')
    ordering = ('-uploaded_at',)

@admin.register(StandardDocumentLink)
class StandardDocumentLinkAdmin(admin.ModelAdmin):
    list_display = ('standard_section', 'document', 'compliance_status', 'created_at')
    list_filter = ('compliance_status', 'standard_section__standard')
    search_fields = ('standard_section__code', 'document__title', 'notes')
    ordering = ('standard_section__code', 'document__title')

@admin.register(StandardCompliance)
class StandardComplianceAdmin(admin.ModelAdmin):
    list_display = ('requirement', 'status', 'user', 'recorded_at')
    list_filter = ('status', 'requirement__section__standard')
    search_fields = ('requirement__code', 'notes')
    ordering = ('-recorded_at',)

@admin.register(StandardRevision)
class StandardRevisionAdmin(admin.ModelAdmin):
    list_display = ('content_object', 'change_type', 'changed_by', 'timestamp')
    list_filter = ('change_type',)
    search_fields = ('change_reason', 'diff')
    ordering = ('-timestamp',)

# Register StandardCategory model
admin.site.register(StandardCategory, StandardCategoryAdmin)
