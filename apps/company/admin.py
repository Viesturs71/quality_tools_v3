from django.contrib import admin
from django.contrib.admin import AdminSite
from django.utils.translation import gettext_lazy as _
from typing import ClassVar
from apps.company.models import Company, Department, Location


# Create a custom admin site
class CustomAdminSite(AdminSite):
    site_header = _("Management System Tools Admin")
    site_title = _("Management System Tools Admin Portal")
    index_title = _("Welcome to Management System Tools")


# Initialize the custom admin site
custom_admin_site = CustomAdminSite(name='custom_admin')

class DepartmentInline(admin.TabularInline):
    model = Department
    extra = 1
    fields: ClassVar[tuple] = ('name', 'manager', 'description')


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1
    fields: ClassVar[tuple] = ('name', 'address', 'city', 'country', 'is_headquarters')

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['name', 'registration_number', 'country_name', 'is_active']
    list_filter = ['is_active']  # Removed invalid country_code field reference
    search_fields = ['name', 'registration_number']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = [
        (_('Basic Information'), {
            'fields': ['name', 'registration_number', 'vat_number', 'logo']
        }),
        (_('Contact Details'), {
            'fields': ['email', 'phone', 'website']
        }),
        (_('Address'), {
            'fields': ['address_line1', 'address_line2', 'city', 'postal_code']
        }),
        (_('Status'), {
            'fields': ['is_active', 'created_at', 'updated_at']
        }),
    ]
    
    def country_name(self, obj):
        """Display country name for list view"""
        return getattr(obj, 'country', '')
    country_name.short_description = _('Country')

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'manager_name', 'is_active']
    list_filter = ['company', 'is_active']
    search_fields = ['name', 'company__name']
    fieldsets = [
        (_('Basic Information'), {
            'fields': ['name', 'company', 'description']
        }),
        (_('Management'), {
            'fields': ['manager_id', 'parent_department']
        }),
        (_('Status'), {
            'fields': ['is_active']
        }),
    ]
    
    def manager_name(self, obj):
        """Display manager name for list view"""
        if hasattr(obj, 'manager'):
            return str(obj.manager)
        return "-"
    manager_name.short_description = _('Manager')
    manager_name.admin_order_field = 'manager_id'

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['name', 'company', 'address_line', 'city_name', 'country_name']
    list_filter = ['company']  # Removed invalid country_code field reference
    search_fields = ['name', 'address_line1', 'city']
    
    fieldsets = [
        (_('Basic Information'), {
            'fields': ['name', 'company', 'description']
        }),
        (_('Address'), {
            'fields': ['address_line1', 'address_line2', 'city', 'postal_code']
        }),
        (_('Contact'), {
            'fields': ['phone', 'email']
        }),
        (_('Coordinates'), {
            'fields': ['latitude', 'longitude'],
            'classes': ['collapse']
        }),
    ]
    
    def address_line(self, obj):
        """Display address line for list view"""
        return obj.address_line1
    address_line.short_description = _('Address')
    
    def city_name(self, obj):
        """Display city for list view"""
        return obj.city
    city_name.short_description = _('City')
    
    def country_name(self, obj):
        """Display country name for list view"""
        return getattr(obj, 'country', '')
    country_name.short_description = _('Country')
