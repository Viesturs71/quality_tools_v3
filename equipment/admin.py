from django.contrib import admin
from .models import (
    Department,
    Equipment,
    EquipmentType,
    MaintenanceRecord,
    EquipmentDocument,
    EquipmentRegistry,
)

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', )  # Izņemti neeksistējošie 'code', 'is_active'
    list_filter = ()  # Iepriekš bija kļūdains: (')
    search_fields = ('name', )  # 'code', 'description' izņemti, ja nav modelī
    ordering = ('name', )

@admin.register(Equipment)
class EquipmentAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'inventory_number', 'serial_number',
        'location', 'status', 'is_measuring_instrument'
    ]
    list_filter = ['status', 'is_measuring_instrument', 'department']
    search_fields = ['name', 'inventory_number', 'serial_number', 'location']
    fieldsets = [
        ('General Information', {
            'fields': [
                'name', 'equipment_type', 'model', 'type_details', 'manufacturer',
                'inventory_number', 'serial_number', 'location'
            ]
        }),
        ('Department Information', {
            'fields': ['department', 'responsible_person']
        }),
        ('Dates and Financial Information', {
            'fields': ['manufacture_date', 'purchase_date', 'purchase_price']
        }),
        ('Metrological Control', {
            'fields': [
                'is_measuring_instrument', 'metrological_control_type',
                'metrological_control_institution', 'certificate_number',
                'certificate_date', 'control_periodicity', 'next_verification_date'
            ],
            'classes': ['collapse'],
        }),
        ('Status Information', {
            'fields': ['status', 'additional_info', 'notes']
        }),
    ]

@admin.register(EquipmentDocument)
class EquipmentDocumentAdmin(admin.ModelAdmin):
    list_display = ['document', 'equipment', 'uploaded_by', 'uploaded_at']  # 'title', 'description' noņemti, ja nav modelī
    list_filter = ['document_type']  # Pielāgots, ja 'document_type' ir caur `document`
    search_fields = ['document__title', 'document__internal_reference']  # Ja 'description' nav, jāizņem
    date_hierarchy = 'uploaded_at'

@admin.register(MaintenanceRecord)
class MaintenanceRecordAdmin(admin.ModelAdmin):
    list_display = ['maintenance_date', 'maintenance_type', 'equipment', 'performed_by', 'next_maintenance_date']
    list_filter = ['maintenance_type', 'maintenance_date']
    search_fields = ['equipment__name', 'equipment__inventory_number', 'performed_by', 'description']
    date_hierarchy = 'maintenance_date'

@admin.register(EquipmentType)
class EquipmentTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_measuring_instrument', 'is_active']
    list_filter = ['is_measuring_instrument', 'is_active']
    search_fields = ['name', 'description']

@admin.register(EquipmentRegistry)
class EquipmentRegistryAdmin(admin.ModelAdmin):
    list_display = ('equipment', 'authorized_user', 'authorized_since')  # tikai esoši lauki!
