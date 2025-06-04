"""Admin configuration for the company app."""

from django.contrib import admin
from .models import Company, Department, Location
from django.utils import timezone
from accounts.admin import custom_admin_site



@admin.register(Company, site=custom_admin_site)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ("name", "code")

@admin.register(Department, site=custom_admin_site)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name", "company")

@admin.register(Location, site=custom_admin_site)
class LocationAdmin(admin.ModelAdmin):
    list_display = ("name", "address")


# Register models with both the default admin site and the custom admin site so
# that navigation links work regardless of which admin interface is used.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Location, LocationAdmin)

custom_admin_site.register(Company, CompanyAdmin)
custom_admin_site.register(Department, DepartmentAdmin)
custom_admin_site.register(Location, LocationAdmin)

