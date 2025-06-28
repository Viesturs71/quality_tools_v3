from django.contrib import admin
from .models import (
    Method, 
    ExternalQualityControl,
    InternalQualityControl,
    MethodVerification
)


@admin.register(Method)
class MethodAdmin(admin.ModelAdmin):
    list_display = ('name', 'identification', 'investigation_field', 'verification_date', 'created_at')
    search_fields = ('name', 'identification', 'investigation_field')
    list_filter = ('investigation_field', 'verification_date')
    readonly_fields = ('created_at', 'updated_at', 'created_by')
    fieldsets = (
        (None, {
            'fields': ('name', 'identification', 'investigation_field', 'analyzer', 'technology', 'test_material')
        }),
        ('Quality Control', {
            'fields': ('internal_qc_required', 'external_qc_required', 'verification_required',
                       'last_internal_qc_date', 'last_external_qc_date', 'verification_date', 'next_verification_date')
        }),
        ('Additional Information', {
            'fields': ('location', 'document', 'created_by', 'created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # If creating a new record
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


@admin.register(ExternalQualityControl)
class ExternalQualityControlAdmin(admin.ModelAdmin):
    list_display = ('service_provider', 'laboratory', 'code', 'quantity', 'price', 'test_amount')
    search_fields = ('service_provider', 'laboratory', 'code')
    list_filter = ('service_provider', 'laboratory')


@admin.register(InternalQualityControl)
class InternalQualityControlAdmin(admin.ModelAdmin):
    list_display = ('method', 'control_date', 'control_material', 'result', 'is_conforming', 'performed_by')
    search_fields = ('method__name', 'control_material', 'performed_by')
    list_filter = ('is_conforming', 'control_date')
    date_hierarchy = 'control_date'


@admin.register(MethodVerification)
class MethodVerificationAdmin(admin.ModelAdmin):
    list_display = ('method', 'verification_type', 'verification_date', 'performed_by', 'is_approved')
    search_fields = ('method__name', 'performed_by')
    list_filter = ('verification_type', 'is_approved')
    date_hierarchy = 'verification_date'
    fieldsets = (
        (None, {
            'fields': ('method', 'verification_type', 'verification_date', 'performed_by')
        }),
        ('Performance Characteristics', {
            'fields': ('precision_data', 'accuracy_data', 'linearity_data', 'detection_limit', 'quantitation_limit')
        }),
        ('Results', {
            'fields': ('acceptance_criteria', 'results_summary', 'is_approved', 'approved_by', 'approval_date')
        }),
        ('Documents', {
            'fields': ('protocol_document', 'report_document')
        }),
    )
