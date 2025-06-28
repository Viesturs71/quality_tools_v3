from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Document, DocumentSection, Attachment


class DocumentSectionInline(admin.TabularInline):
    model = DocumentSection
    extra = 1
    fields = ('title', 'content', 'order')


class AttachmentInline(admin.TabularInline):
    model = Attachment
    extra = 1
    fields = ('file', 'description')


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'document_number', 'version', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'updated_at')
    search_fields = ('title', 'document_number', 'description')
    date_hierarchy = 'created_at'
    inlines = [DocumentSectionInline, AttachmentInline]
    fieldsets = (
        (None, {
            'fields': ('title', 'document_number', 'version', 'status')
        }),
        (_('Content'), {
            'fields': ('description', 'content')
        }),
        (_('Metadata'), {
            'fields': ('author', 'reviewers', 'approver')
        }),
        (_('Dates'), {
            'fields': ('effective_date', 'review_date', 'expiry_date')
        })
    )


class DocumentSectionAdmin(admin.ModelAdmin):
    list_display = ('code', 'title_original', 'title_alt', 'document', 'parent', 'order')
    list_filter = ('document', 'parent')
    search_fields = (
        'code', 'title_original', 'title_alt', 'content_original', 'content_alt', 'document__title'
    )
    fieldsets = (
        (None, {
            'fields': ('document', 'parent', 'code', 'title_original', 'title_alt', 'order')
        }),
        (_('Content'), {
            'fields': ('content_original', 'content_alt')
        }),
    )


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('file', 'document', 'description', 'uploaded_at')
    list_filter = ('document', 'uploaded_at')
    search_fields = ('description', 'document__title')
    fieldsets = (
        (None, {
            'fields': ('document', 'file')
        }),
        (_('Details'), {
            'fields': ('description',)
        })
    )


admin.site.register(Document, DocumentAdmin)
admin.site.register(DocumentSection, DocumentSectionAdmin)
admin.site.register(Attachment, AttachmentAdmin)
