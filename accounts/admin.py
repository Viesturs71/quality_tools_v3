"""
Admin configuration for accounts app.
"""
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from myproject.admin import custom_admin_site

User = get_user_model()

# ============================
# Pielāgots admin site
# ============================

# Use the project's custom admin site for all registrations

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
