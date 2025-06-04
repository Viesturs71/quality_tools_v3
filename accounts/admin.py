"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
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
            "quality_docs": _("Documentation"),
            "methods": _("Method Management"),
            "equipment": _("Equipment Registry"),
            "staff": _("Personnel Management"),
            "audits": _("Audits"),
            "risks": _("Risk Management"),
            "kpi": _("KPI Management"),
        }
        return sorted(app_list, key=lambda x: custom_order.get(x["app_label"], x["name"]))


custom_admin_site = CustomAdminSiteWithLanguageSwitcher(name="custom_admin")

# 👥 User Management
@admin.register(User, site=custom_admin_site)
class CustomUserAdmin(UserAdmin):
    """Customized user administration with additional fields and filters."""
    list_display = ("username", "email", "is_active", "is_staff")
    list_filter = ("is_staff", "groups")
    search_fields = ("username", "email")
    ordering = ["username"]


# 🛠️ Other model registrations
custom_admin_site.register(Group)
custom_admin_site.register(Permission)
