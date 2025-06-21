from django.contrib import admin
from django.contrib.admin import AdminSite
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group, Permission
from django.utils.translation import gettext_lazy as _

# Importēt modeļus
from accounts.models import CustomUser
from equipment.models.equipment_registry import EquipmentRegistry
from personnel.models import Department, Education, Employee, Field, Position
from quality_docs.models import (
    Company,
    DocumentSection,
    DocumentType,
    QualityDocument,
    Standard,
    StandardSection,
)


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    fieldsets = (*UserAdmin.fieldsets, (None, {'fields': ('phone_number',)}))


class StandardAdmin(admin.ModelAdmin):
    list_display = ["standard_number", "title", "version", "created_at"]
    search_fields = ["standard_number", "title"]
    ordering = ["standard_number"]


class StandardSectionAdmin(admin.ModelAdmin):
    list_display = ("title", "parent", "created_at")
    search_fields = ("title",)
    ordering = ["code"]


class EquipmentRegistryAdmin(admin.ModelAdmin):
    list_display = (
        "equipment_name",
        "model_manufacturer",
        "inventory_number",
        "serial_number",
        "manufacture_date",
        "purchase_date",
        "purchase_price",
        "location",
    )
    search_fields = ("equipment_name", "model_manufacturer", "inventory_number")
    ordering = ["-created_at"]


class QualityDocumentAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'document_type', 'version', 'status',
        'publication_date', 'approval_date', 'review_date'
    ]
    list_filter = [
        'document_type', 'status',
        'publication_date', 'approval_date', 'review_date'
    ]
    search_fields = ['title', 'version', 'document_identifier']
    ordering = ['-publication_date']


class CustomAdminSite(AdminSite):
    site_header = _("Management System Tools")
    site_title = _("Administration Panel")
    index_title = _("System Management")

    def each_context(self, request):
        context = super().each_context(request)
        context['extra_css'] = """
        <style>
            #site-name {
                font-size: 200% !important;
            }
        </style>
        """
        return context

    def get_app_list(self, request, app_label=None):
        """
        Nodrošina pilnu, strukturētu sadaļu un modeļu sarakstu.
        Sagrupē aplikācijas un modeļus zem atbilstošajiem virsrakstiem.
        """
        app_dict = self._build_app_dict(request)

        custom_order = [
            ("accounts", _("User Management")),
            ("quality_docs", _("Documentation")),
            ("methods", _("Method Management")),
            ("equipment", _("Equipment Registry")),
            ("personnel", _("Staff Management")),
            ("audits", _("Audits")),
            ("risks", _("Risk Management")),
            ("kpi", _("KPI Management")),
        ]

        ordered_app_list = []
        for app_label, display_name in custom_order:
            app = app_dict.get(app_label)
            if app:
                app["name"] = display_name
                app["models"].sort(key=lambda x: x["name"])
                ordered_app_list.append(app)

        # Papildus aplikācijas, kas nav definētas
        remaining_apps = [
            app for label, app in app_dict.items()
            if label not in dict(custom_order)
        ]
        ordered_app_list.extend(sorted(remaining_apps, key=lambda x: x["name"]))

        return ordered_app_list


# Inicializē pielāgoto admin vietni
custom_admin_site = CustomAdminSite(name="custom_admin")

# Reģistrācija
custom_admin_site.register(CustomUser, CustomUserAdmin)
custom_admin_site.register(Group)
custom_admin_site.register(Permission)
custom_admin_site.register(Standard, StandardAdmin)
custom_admin_site.register(StandardSection, StandardSectionAdmin)
custom_admin_site.register(DocumentType)
custom_admin_site.register(QualityDocument, QualityDocumentAdmin)
custom_admin_site.register(DocumentSection)
custom_admin_site.register(Company)
custom_admin_site.register(EquipmentRegistry, EquipmentRegistryAdmin)
custom_admin_site.register(Department)
custom_admin_site.register(Position)
custom_admin_site.register(Field)
custom_admin_site.register(Education)
custom_admin_site.register(Employee)
