from django.contrib import admin
from django.contrib.auth.admin import GroupAdmin, UserAdmin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group, Permission
from django.urls import path
from django.utils.translation import gettext_lazy as _
from django.views.i18n import set_language
from django_mptt_admin.admin import DjangoMpttAdmin

from accounts.models import CustomUser
from quality_docs.models import DocumentType, QualityDocument
from quality_docs.models.standards import Standard, StandardSection


# Reģistrē nepieciešamos modeļus ar standarta admin
def register_with_custom_admin():
    from accounts.custom_admin import custom_admin_site

    custom_admin_site.register(Permission)


# Pielāgots administrācijas panelis
class CustomAdminSite(admin.AdminSite):
    site_header = _("Management System Tools")
    site_title = _("Administration")
    index_title = _("System Management")

    def get_app_list(self, request, app_label=None):
        app_list = super().get_app_list(request, app_label)
        custom_order = {
            "quality_docs": _("Documentation"),
            "methods": _("Method Management"),
            "equipment": _("Equipment Registry"),
            "staff": _("Staff Management"),
            "audits": _("Audits"),
            "risks": _("Risk Management"),
            "kpi": _("KPI Management"),
        }
        return sorted(
            app_list, key=lambda x: custom_order.get(x["app_label"], x["name"])
        )


# Administrācijas panelis ar valodu maiņu
class CustomAdminSiteWithLanguageSwitcher(CustomAdminSite):
    def get_urls(self):
        urls = super().get_urls()
        return [path("set_language/", set_language, name="set_language"), *urls]


# Inicializē pielāgoto admin paneli
custom_admin_site = CustomAdminSiteWithLanguageSwitcher(name="custom_admin")


# Dokumentācijas modeļu reģistrācija
class StandardSectionInline(admin.StackedInline):
    model = StandardSection
    extra = 1


class StandardAdmin(admin.ModelAdmin):
    list_display = ["standard_number", "title", "version", "created_at"]
    search_fields = ["standard_number", "title"]
    ordering = ["standard_number"]


class StandardSectionAdmin(DjangoMpttAdmin):
    list_display = ("title", "parent", "created_at")
    search_fields = ("title",)
    ordering = ["code"]


# Lietotāju pārvaldība ar pielāgotu admin klasi
class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active", "groups")


# Ja `User` modelis nav reģistrēts custom_admin_site, reģistrē to
if CustomUser in custom_admin_site._registry:
    custom_admin_site.unregister(CustomUser)
custom_admin_site.register(CustomUser, CustomUserAdmin)


# Pārējo modeļu reģistrācija
custom_admin_site.register(Standard, StandardAdmin)
custom_admin_site.register(StandardSection, StandardSectionAdmin)
custom_admin_site.register(DocumentType)
custom_admin_site.register(Group, GroupAdmin)

class CustomUserAdmin(UserAdmin):
    """
    Admin interface for CustomUser model.
    """
    # Add company to list display and fieldsets
    list_display = ('username', 'email', 'first_name', 'last_name', 'company', 'is_staff')

    # Add company to the fieldsets
    fieldsets = (*UserAdmin.fieldsets, ('Company Information', {'fields': ('company',)}))

    add_fieldsets = (*UserAdmin.add_fieldsets, ('Company Information', {'fields': ('company',)}))

admin.site.register(CustomUser, CustomUserAdmin)
