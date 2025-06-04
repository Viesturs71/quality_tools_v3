#personnel/admin.py
from django.contrib import admin
from django.forms import ModelForm

from .models import Department, Education, Employee, Field, Position


class PositionForm(ModelForm):
    class Meta:
        model = Position
        fields = ['name', 'description']  # Changed 'title' to 'name' to match the model field

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    form = PositionForm
    list_display = ['name', 'description']  # Changed 'title' to 'name' here too if needed
    search_fields = ['name', 'description']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'description']
    list_filter = ['company']
    search_fields = ['name', 'description']

@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

@admin.register(Field)
class FieldAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    search_fields = ['name', 'description']

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'department', 'position', 'hire_date']
    list_filter = ['department', 'position', 'hire_date']
    search_fields = ['first_name', 'last_name', 'email']
