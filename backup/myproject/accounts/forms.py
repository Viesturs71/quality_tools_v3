# accounts/forms.py
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.utils.translation import gettext_lazy as _

User = get_user_model()

class RegisterForm(UserCreationForm):
    """
    Custom registration form extending Django's UserCreationForm.
    """
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')})
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add form-control class for Bootstrap styling
        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})

"""
accounts/admin.py
Customized Django admin panel with additional functionality.
"""

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.i18n import set_language
from django_mptt_admin.admin import DjangoMpttAdmin

from quality_docs.models.documents import DocumentType, QualityDocument
from quality_docs.models.standards import Standard, StandardSection

User = get_user_model()


# 🛡️ Customized admin panel with language switching
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


# 📝 Documentation model administration
class StandardSectionInline(admin.StackedInline):
    """Allows editing of standard sections directly from the standard edit page."""
    model = StandardSection
    extra = 1


@admin.register(Standard, site=custom_admin_site)
class StandardAdmin(admin.ModelAdmin):
    """Standard administration with inlines and search capabilities."""
    inlines = [StandardSectionInline]
    list_display = ("standard_number", "title", "version")
    search_fields = ("standard_number", "title", "version")
    ordering = ["standard_number"]


@admin.register(StandardSection, site=custom_admin_site)
class StandardSectionAdmin(DjangoMpttAdmin):
    """Standard section management with hierarchical representation."""
    list_display = ("title", "parent", "created_at")
    search_fields = ("title",)
    ordering = ["code"]


# 👥 User Management
@admin.register(User, site=custom_admin_site)
class CustomUserAdmin(UserAdmin):
    """Customized user administration with additional fields and filters."""
    fieldsets = (*UserAdmin.fieldsets, (_("Company Information"), {"fields": ("company",)}))
    list_display = ("username", "email", "company", "is_active", "is_staff")
    list_filter = ("company", "is_staff", "groups")
    search_fields = ("username", "email", "company__name")
    ordering = ["username"]


# 🛠️ Other model registrations
custom_admin_site.register(DocumentType)
custom_admin_site.register(Group)
custom_admin_site.register(Permission)
