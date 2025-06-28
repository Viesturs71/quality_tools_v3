from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Equipment,
    EquipmentCategory,
    EquipmentDocument,
    EquipmentType,
    MaintenanceRecord,
    Department,
)
from apps.documents.models import Document  # Updated from apps.quality_docs.models


@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    # Fix list_display to use fields that actually exist
    list_display = ['name', 'serial_number', 'purchase_date']  # Removed 'category'
    search_fields = ['name', 'serial_number']
    # Fix list_filter to use existing fields
    list_filter = ['purchase_date']  # Removed 'category'


@admin.register(EquipmentCategory)
class EquipmentCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']


@admin.register(EquipmentDocument)
class EquipmentDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'equipment', 'uploaded_by', 'uploaded_at']
    search_fields = ['title', 'description']
    list_filter = ['uploaded_at']


@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_measuring_instrument', 'is_active']
    search_fields = ['name']
    list_filter = ['is_measuring_instrument', 'is_active']


@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    # Fixed field names in list_display and list_filter
    list_display = ['date', 'equipment', 'maintenance_type']  # Changed 'maintenance_date' to 'date'
    list_filter = ['maintenance_type', 'date']  # Changed 'maintenance_date' to 'date'
    search_fields = ['equipment__name', 'description']
    autocomplete_fields = ['equipment']


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    fieldsets = (
        (_('Calibration'), {  # Translated to English
            'fields': ('needs_calibration', 'calibration_frequency', 'next_calibration_date')
        }),
        (_('Responsibility'), {  # Translated to English
            'fields': ('responsible_person',)
        }),
    )
    search_fields = ('description', 'results', 'certificate_number')

    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new record
            obj.performed_by = request.user
        super().save_model(request, obj, form, change)
