from django.contrib import admin
from apps.authentication.models.one_time_password import OneTimePassword

@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    readonly_fields = ('code',)
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_valid')
    search_fields = ('user__username', 'code')