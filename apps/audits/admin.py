from django.contrib import admin
from .models import Audit


@admin.register(Audit)
class AuditAdmin(admin.ModelAdmin):
    list_display = ('title', 'date', 'status', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'date')
    ordering = ('-date',)
