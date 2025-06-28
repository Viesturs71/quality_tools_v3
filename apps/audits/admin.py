from django.contrib import admin
from .models import Audit, AuditFinding, AuditChecklist


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'date')
    ordering = ('-date',)


@admin.register(AuditFinding)
class AuditFindingAdmin(admin.ModelAdmin):
    list_display = ('audit', 'severity', 'description', 'created_at')
    list_filter = ('severity', 'audit')
    search_fields = ('description', 'reference')


@admin.register(AuditChecklist)
class AuditChecklistAdmin(admin.ModelAdmin):
    list_display = ('audit', 'category', 'question', 'status')
    list_filter = ('status', 'category', 'audit')
    search_fields = ('question', 'comments')
