# methods/admin/__init__.py
from django.contrib import admin
from django.contrib.admin.sites import NotRegistered

from accounts.custom_admin import custom_admin_site
from methods.models import MetozuRegistrs


class MetozuRegistrsAdmin(admin.ModelAdmin):
    list_display = ['name', 'identification', 'investigation_field', 'created_at']
    search_fields = ['name', 'identification', 'investigation_field']
    list_filter = ['investigation_field', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

def register_metozu_registrs():
    """Droša MetozuRegistrs modeļa reģistrācija"""
    try:
        # Mēģinām atreģistrēt, ja jau reģistrēts
        custom_admin_site.unregister(MetozuRegistrs)
    except NotRegistered:
        pass

    if not custom_admin_site._registry.get(MetozuRegistrs):
        custom_admin_site.register(MetozuRegistrs, MetozuRegistrsAdmin)

# Izsaucam reģistrācijas funkciju
register_metozu_registrs()
