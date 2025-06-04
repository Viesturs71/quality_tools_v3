"""Admin configuration for the company app."""

from django.contrib import admin

from myproject.admin import custom_admin_site

from .models import Company, Department, Location


class CompanyAdmin(admin.ModelAdmin):
    """Administration options for the ``Company`` model."""

    list_display = ("name", "code")


class DepartmentAdmin(admin.ModelAdmin):
    """Administration options for the ``Department`` model."""

    list_display = ("name", "company")


class LocationAdmin(admin.ModelAdmin):
    """Administration options for the ``Location`` model."""

    list_display = ("name", "address")


# Register models with both the default admin site and the custom admin site so
# that navigation links work regardless of which admin interface is used.
admin.site.register(Company, CompanyAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Location, LocationAdmin)

custom_admin_site.register(Company, CompanyAdmin)
custom_admin_site.register(Department, DepartmentAdmin)
custom_admin_site.register(Location, LocationAdmin)

