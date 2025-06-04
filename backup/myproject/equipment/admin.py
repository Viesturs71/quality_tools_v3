from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from .models import (
    Department,
    Equipment,
    EquipmentDocument,
    EquipmentType,
    MaintenanceRecord,
)


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'requires_metrological_control', 'requires_maintenance']
    search_fields = ['name', 'description']
    list_filter = ['requires_metrological_control', 'requires_maintenance']


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'inventory_number', 'serial_number', 'equipment_type', 'location']
    list_filter = ['equipment_type', 'location', 'technical_status']
    search_fields = ['equipment_name', 'inventory_number', 'serial_number']
    date_hierarchy = 'created_at'


@admin.register(EquipmentDocument)
class EquipmentDocumentAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'document_type', 'title', 'created_at')
    list_filter = ('document_type', 'created_at')
    search_fields = ('title', 'description')
    date_hierarchy = 'created_at'


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'date_performed', 'maintenance_type', 'performed_by', 'result')
    list_filter = ('maintenance_type', 'date_performed')
    search_fields = ('equipment__equipment_name', 'performed_by', 'description')
    date_hierarchy = 'date_performed'


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    """Admin configuration for Department model."""
    list_display = ('name', 'manager_name')
    search_fields = ('name', 'manager_name', 'description')
    list_filter = ('created_at',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (_('Department Information'), {
            'fields': ('name', 'manager_name', 'description')
        }),
        (_('Metadata'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
