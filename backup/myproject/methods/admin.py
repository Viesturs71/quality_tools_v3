# methods/admin.py
from django.contrib import admin

from .models import AkkRegistrs, MetozuRegistrs


@admin.register(MetozuRegistrs)
class MetozuRegistrsAdmin(admin.ModelAdmin):
    list_display = ('name', 'identification', 'investigation_field', 'verification_date', 'created_at')
    search_fields = ('name', 'identification', 'investigation_field')
    list_filter = ('investigation_field', 'verification_date')
    readonly_fields = ('created_at', 'updated_at', 'created_by')

    def save_model(self, request, obj, form, change):
        if not obj.pk:  # Ja objekts tiek veidots no jauna
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(AkkRegistrs)
class AkkRegistrsAdmin(admin.ModelAdmin):
    list_display = ('pakalpojuma_sniedzejs', 'laboratorija', 'kods', 'skaits', 'cena', 'testa_summa')
    search_fields = ('pakalpojuma_sniedzejs', 'laboratorija', 'kods')
    list_filter = ('pakalpojuma_sniedzejs', 'laboratorija')
