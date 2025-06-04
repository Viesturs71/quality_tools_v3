# quality_docs/admin.py

from django.contrib import admin
from django.db.models import IntegerField
from django.db.models.functions import Cast
from django.shortcuts import redirect
from django.urls import path, reverse
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.db.models import Count
from mptt.admin import MPTTModelAdmin

from .models import DocumentType, QualityDocument, DocumentSection, DocumentReview


# --------------- Inline modeļi ---------------
class DocumentSectionInline(admin.TabularInline):
    model = DocumentSection
    extra = 1

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(numeric_ordering=Cast('identifier', IntegerField())).order_by('numeric_ordering')


# --------------- Dokumentu tipi ---------------
@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'abbreviation', 'description']
    search_fields = ['name', 'abbreviation']
    ordering = ['name']
    fields = ['name', 'abbreviation', 'description']

    def get_readonly_fields(self, request, obj=None):
        return ('abbreviation',) if obj else []


# --------------- Kvalitātes dokumenti ---------------
@admin.register(QualityDocument)
class QualityDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'document_type', 'version', 'status', 'created_at', 'author']
    list_filter = ['document_type', 'status', 'created_at', 'updated_at']
    search_fields = ['title', 'content', 'author__username']
    ordering = ['-created_at']
    readonly_fields = ['created_at', 'updated_at']

    fieldsets = (
        (_('Document Information'), {
            'fields': ('title', 'document_type', 'content', 'version')
        }),
        (_('Workflow'), {
            'fields': ('status', 'author', 'owner', 'approver')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def add_view(self, request, form_url='', extra_context=None):
        return redirect('quality_docs:document_create')

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('add/', self.add_view, name='quality_docs_qualitydocument_add'),
        ]
        return custom_urls + urls


# --------------- Dokumentu sadaļas ---------------
@admin.register(DocumentSection)
class DocumentSectionAdmin(MPTTModelAdmin):
    list_display = ['name', 'identifier', 'parent']
    search_fields = ['name', 'identifier']
    list_filter = ['parent', 'identifier']
    list_editable = ('identifier',)
    list_display_links = ('name',)
    mptt_level_indent = 20

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(numeric_ordering=Cast('identifier', IntegerField())).order_by('numeric_ordering')

    def document_count(self, obj):
        return obj.documents.count()
    document_count.short_description = _("Documents")


# --------------- Atsauksmes (Review) ---------------
@admin.register(DocumentReview)
class DocumentReviewAdmin(admin.ModelAdmin):
    list_display = ['document', 'reviewer', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['document__title', 'reviewer__username', 'comments']
    ordering = ['-created_at']
    readonly_fields = ['created_at']

    fieldsets = (
        (_('Review Information'), {
            'fields': ('document', 'reviewer', 'status')
        }),
        (_('Comments'), {
            'fields': ('comments',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at',),
            'classes': ('collapse',)
        })
    )
