from django.contrib import admin
from .models import Employee, Qualification, Training, EmployeeRecord, Education


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee_id', 'first_name', 'last_name', 'position', 'department', 'is_active')
    search_fields = ('employee_id', 'first_name', 'last_name', 'position', 'email')
    list_filter = ('is_active', 'department', 'hire_date')
    ordering = ('last_name', 'first_name')


@admin.register(Qualification)
class QualificationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'qualification_type', 'issue_date', 'expiry_date', 'issuing_organization')
    search_fields = ('employee__first_name', 'employee__last_name', 'qualification_type', 'certificate_number')
    list_filter = ('qualification_type', 'issue_date', 'expiry_date')


@admin.register(Training)
class TrainingAdmin(admin.ModelAdmin):
    list_display = ('employee', 'training_name', 'start_date', 'end_date', 'status', 'certificate_issued')
    search_fields = ('employee__first_name', 'employee__last_name', 'training_name', 'provider')
    list_filter = ('status', 'start_date', 'end_date', 'certificate_issued')


@admin.register(EmployeeRecord)
class EmployeeRecordAdmin(admin.ModelAdmin):
    list_display = ('employee', 'record_type', 'title', 'issue_date', 'expiry_date', 'is_confidential')
    search_fields = ('employee__first_name', 'employee__last_name', 'title', 'record_type')
    list_filter = ('record_type', 'issue_date', 'expiry_date', 'is_confidential')


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ('employee', 'institution', 'level', 'field_of_study', 'degree', 'is_completed')
    search_fields = ('employee__first_name', 'employee__last_name', 'institution', 'degree')
    list_filter = ('level', 'is_completed', 'start_date', 'end_date')
