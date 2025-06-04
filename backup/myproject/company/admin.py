### 📄 company/admin.py**

from django.contrib import admin

from .models import Company, Department


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    """Uzņēmuma pārvaldība Django administrācijas panelī."""

    list_display = (
        "name",
        "phone",
        "email",
        "website",
    )
    search_fields = ("name", "email")

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'manager')
    list_filter = ('company',)
    search_fields = ('name', 'description', 'manager')
