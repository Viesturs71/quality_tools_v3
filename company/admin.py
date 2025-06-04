from django.contrib import admin
from .models import Company, Department, Location
from django.utils import timezone
from myproject.admin import custom_admin_site



@admin.register(Company, site=custom_admin_site)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "code")

@admin.register(Department, site=custom_admin_site)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "company")

@admin.register(Location, site=custom_admin_site)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address")

