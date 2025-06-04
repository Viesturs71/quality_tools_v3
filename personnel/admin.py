"""
Admin configuration for personnel app
"""
from django.contrib import admin
from .models import Employee, Qualification, Training, EmployeeRecord, Education
from accounts.admin import custom_admin_site

class EmployeeRecordInline(admin.TabularInline):
    model = EmployeeRecord
    extra = 1


@admin.register(Employee, site=custom_admin_site)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['employee_id', 'first_name', 'last_name', 'position', 'department', 'is_active']
    list_filter = ['is_active', 'department', 'position']
    search_fields = ['employee_id', 'first_name', 'last_name', 'email']
    fieldsets = (
        (None, {
            'fields': ('employee_id', 'first_name', 'last_name', 'user')
        }),
        ('Employment Information', {
            'fields': ('position', 'department', 'hire_date', 'is_active')
        }),
        ('Contact Information', {
            'fields': ('email', 'phone')
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )


@admin.register(Qualification, site=custom_admin_site)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'qualification_type', 'issue_date', 'expiry_date']
    list_filter = ['qualification_type', 'issuing_organization']
    search_fields = ['employee__first_name', 'employee__last_name', 'qualification_type']


@admin.register(Training, site=custom_admin_site)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ['employee', 'training_name', 'start_date', 'end_date', 'status']
    list_filter = ['status', 'provider']
    search_fields = ['employee__first_name', 'employee__last_name', 'training_name']


@admin.register(EmployeeRecord, site=custom_admin_site)
class EmployeeRecordAdmin(admin.ModelAdmin):
    list_display = ['employee', 'record_type', 'title', 'issue_date', 'is_confidential']
    list_filter = ['record_type', 'is_confidential']
    search_fields = ['employee__first_name', 'employee__last_name', 'title']
    fieldsets = (
        (None, {
            'fields': ('employee', 'record_type', 'title', 'description')
        }),
        ('Document Information', {
            'fields': ('issue_date', 'expiry_date', 'document')
        }),
        ('Security', {
            'fields': ('is_confidential',)
        }),
        ('Additional Information', {
            'fields': ('notes',)
        }),
    )


@admin.register(Education, site=custom_admin_site)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['employee', 'level', 'institution', 'degree', 'is_completed']
    list_filter = ['level', 'is_completed']
    search_fields = ['employee__first_name', 'employee__last_name', 'institution', 'degree']
    fieldsets = (
        (None, {
            'fields': ('employee', 'level', 'institution')
        }),
        ('Degree Information', {
            'fields': ('field_of_study', 'degree', 'start_date', 'end_date', 'is_completed')
        }),
        ('Documentation', {
            'fields': ('description', 'document')
        }),
    )


