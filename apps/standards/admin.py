from django.contrib import admin
from .models import (
    Standard,
    StandardAttachment,
    StandardDocument,
    StandardRequirement,
    StandardRevision,
    StandardSection,
)

@admin.register(Standard)
class StandardAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'is_active')
    search_fields = ('number', 'title')

@admin.register(StandardSection)
class StandardSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'parent']
    search_fields = ['title', 'description']
    list_filter = ['parent']
