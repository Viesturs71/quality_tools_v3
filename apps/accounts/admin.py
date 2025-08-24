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
from .models import UserPermission, Account, AccountMembership, Subscription

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
        
        # Define the custom order with correct app labels
        custom_order = {
            "documents": 1,  # Documentation
            "methods": 2,    # Method Management
            "equipment": 3,  # Equipment Registry
            "personnel": 4,  # Personnel Management
            "audits": 5,     # Audits
            "risks": 6,      # Risk Management
            "kpi": 7,        # KPI Management
            "accounts": 8,   # User accounts
            "auth": 9,       # Authentication and permissions
            "admin": 10,     # Admin functionality
        }
        
        # Sort the app list by the priority defined in custom_order
        # Apps not in custom_order will be placed at the end
        return sorted(
            app_list,
            key=lambda x: custom_order.get(x["app_label"], 100)
        )


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

# Only register UserPermission once
class UserPermissionAdmin(admin.ModelAdmin):
    """Admin configuration for UserPermission model"""
    list_display = ('user', 'can_approve_documents', 'can_manage_users', 'can_export_data')
    list_filter = ('can_approve_documents', 'can_manage_users', 'can_export_data')
    search_fields = ('user__username', 'user__email')
    fieldsets = (
        (None, {'fields': ('user',)}),
        (_('Permissions'), {'fields': ('can_approve_documents', 'can_manage_users', 'can_export_data')}),
    )

# Remove or comment out any duplicate registrations
# The error shows there might be another registration for UserPermission elsewhere in the file
# @admin.register(UserPermission)  # This line is causing the issue - already registered

# Only register the model if it's not already registered
try:
    admin.site.register(UserPermission, UserPermissionAdmin)
except admin.sites.AlreadyRegistered:
    # Model already registered, so skip registration
    pass

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'owner', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'code', 'owner__email')
    readonly_fields = ('created_at', 'updated_at')
    filter_horizontal = ('members',)

    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'description', 'owner', 'is_active')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

@admin.register(AccountMembership)
class AccountMembershipAdmin(admin.ModelAdmin):
    list_display = ('account', 'user', 'role', 'is_active', 'joined_at')
    list_filter = ('role', 'is_active', 'joined_at')
    search_fields = ('account__name', 'user__email')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('account', 'plan', 'status', 'monthly_price', 'next_billing_date')
    list_filter = ('plan', 'status', 'created_at')
    search_fields = ('account__name',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        (None, {
            'fields': ('account', 'plan', 'status')
        }),
        (_('Limits'), {
            'fields': ('max_users', 'max_storage_gb')
        }),
        (_('Billing'), {
            'fields': ('monthly_price', 'trial_ends_at', 'next_billing_date')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
