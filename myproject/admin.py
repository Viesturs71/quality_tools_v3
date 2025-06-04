"""
Custom admin site configuration for the project.
"""
from django.contrib import admin
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.i18n import set_language

class CustomAdminSiteWithLanguageSwitcher(admin.AdminSite):
    site_header = _("Quality Tools Administration")
    site_title = _("Quality Tools Admin")
    index_title = _("System Management")
    
    # Change the name to avoid namespace collision
    name = 'quality_tools_admin'  # Changed from 'custom_admin' to 'quality_tools_admin'
    
    def get_urls(self):
        """Adds a language switching URL to the admin panel."""
        return [path("set_language/", set_language, name="set_language"), *super().get_urls()]

    def get_app_list(self, request, app_label=None):
        """Customizes app ordering in the admin panel."""
        app_list = super().get_app_list(request, app_label)
        custom_order = {
            "accounts": 1,
            "auth": 2,
            "company": 3,
            "equipment": 4,
            "quality_docs": 5,
            "personnel": 6,
            "standards": 7,
        }
        return sorted(app_list, key=lambda x: custom_order.get(x["app_label"], 99))


# Create an instance of the custom admin site
custom_admin_site = CustomAdminSiteWithLanguageSwitcher()
