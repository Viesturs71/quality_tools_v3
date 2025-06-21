from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import Company, Department, Location
from django.contrib.admin import AdminSite


class CustomAdminSite(AdminSite):
    site_header = "Custom Admin"
    site_title = "Custom Admin Portal"
    index_title = "Welcome to the Custom Admin Portal"


custom_admin_site = CustomAdminSite(name='custom_admin')


@admin.register(Company, site=custom_admin_site)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_active', 'created_at')
    search_fields = ('name', 'registration_number')


@admin.register(Department, site=custom_admin_site)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'get_company', 'is_active']  # Updated attributes
    search_fields = ['name']

    def get_company(self, obj):
        return obj.company.name if obj.company else None
    get_company.short_description = _('Company')  # Added method for company

    def is_active(self, obj):
        return obj.active  # Assuming `active` is a field in the Department model
    is_active.boolean = True
    is_active.short_description = _('Is Active')


@admin.register(Location, site=custom_admin_site)
class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'is_active')
    search_fields = ('name', 'address')
