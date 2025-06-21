"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group, Permission, User
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.i18n import set_language

User = get_user_model()

# ============================
# Pielāgots admin site
# ============================

class CustomAdminSiteWithLanguageSwitcher(admin.AdminSite):
    site_header = _("Management System Tools")
    site_title = _("Administration")
    index_title = _("System Management")

    def get_urls(self):
        """Adds a language switching URL to the admin panel."""
        return [path("set_language/", set_language, name="set_language"), *super().get_urls()]

    def get_app_list(self, request, app_label=None):
        """Customizes app ordering in the admin panel."""
        app_list = super().get_app_list(request, app_label)
        custom_order = {
            "documentsquality_docs": _("Documentation"),
            "methods": _("Method Management"),
            "equipment": _("Equipment Registry"),
            "personnel": _("Personnel Management"),
            "audits": _("Audits"),
            "risks": _("Risk Management"),
            "kpi": _("KPI Management"),
        }
        return sorted(app_list, key=lambda x: custom_order.get(x["app_label"], x["name"]))


custom_admin_site = CustomAdminSiteWithLanguageSwitcher(name="custom_admin")

# 🛠️ Other model registrations
custom_admin_site.register(Group)
custom_admin_site.register(Permission)
class EnhancedUserAdmin(BaseUserAdmin):
    """Enhanced User admin with custom sections following the specified admin structure"""
    fieldsets = (
        (_('Authentication'), {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 
                                      'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('username', 'first_name', 'last_name', 'email')

# Try to unregister the User model if it's already registered, then register with our custom admin
try:
    custom_admin_site.unregister(User)
except admin.sites.NotRegistered:
    pass

custom_admin_site.register(User, EnhancedUserAdmin)
