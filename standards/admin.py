from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from mptt.admin import MPTTModelAdmin
from .models.standards import (
    Standard, 
    StandardSection, 
    StandardSubsection, 
    StandardDocument,
    StandardAttachment,
    StandardRevision,
    StandardRequirement,
    StandardComplianceStatus
)
from myproject.admin import custom_admin_site

@admin.register(Standard, site=custom_admin_site)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'publication_year', 'is_active')
    list_filter = ('is_active', 'publication_year')
    search_fields = ('number', 'title', 'description')
    ordering = ('number',)

@admin.register(StandardSection, site=custom_admin_site)
class StandardSectionAdmin(MPTTModelAdmin):
    list_display = ('name', 'standard', 'code', 'order')
    list_filter = ('standard',)
    search_fields = ('name', 'code', 'content')
    raw_id_fields = ('standard',)
    ordering = ('standard', 'order')

@admin.register(StandardSubsection, site=custom_admin_site)
class StandardSubsectionAdmin(admin.ModelAdmin):
    # Fix field references to match actual model fields
    list_display = ('title', 'number', 'section', 'order')  # Changed fields
    list_filter = ('section',)  # Removed 'level'
    search_fields = ('title', 'number', 'content')
    raw_id_fields = ('section',)  # Removed 'parent'
    ordering = ('section', 'order')  # Changed fields

@admin.register(StandardDocument, site=custom_admin_site)
class StandardDocumentAdmin(admin.ModelAdmin):
    # Fix field references to match actual model fields
    list_display = ('title', 'document_type', 'standard', 'version', 'created_at')  # Changed fields
    list_filter = ('document_type', 'standard')
    search_fields = ('title', 'description')
    ordering = ('created_at',)  # Changed from 'uploaded_at'

@admin.register(StandardRequirement, site=custom_admin_site)
class StandardRequirementAdmin(admin.ModelAdmin):
    # Fix field references to match actual model fields
    list_display = ('requirement_id', 'standard', 'section', 'subsection', 'is_mandatory')  # Removed 'priority'
    list_filter = ('standard', 'is_mandatory')  # Removed 'priority'
    search_fields = ('requirement_id', 'description')
    ordering = ('standard', 'requirement_id')

@admin.register(StandardAttachment, site=custom_admin_site)
class StandardAttachmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'standard', 'created_at')
    list_filter = ('standard',)
    search_fields = ('name', 'description')
    ordering = ('standard', 'name')

@admin.register(StandardRevision, site=custom_admin_site)
class StandardRevisionAdmin(admin.ModelAdmin):
    list_display = ('revision_number', 'standard', 'revision_date', 'is_major')
    list_filter = ('standard', 'is_major')
    search_fields = ('revision_number', 'description')
    ordering = ('standard', '-revision_date')

@admin.register(StandardComplianceStatus, site=custom_admin_site)
class StandardComplianceStatusAdmin(admin.ModelAdmin):
    list_display = ('standard', 'requirement', 'status', 'assessed_date', 'next_review_date')
    list_filter = ('standard', 'status')
    search_fields = ('standard__number', 'requirement__requirement_id', 'evidence', 'notes')
    ordering = ('standard', '-assessed_date')
