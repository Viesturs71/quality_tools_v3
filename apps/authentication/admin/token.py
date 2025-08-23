from django.contrib import admin
from apps.authentication.models.token import Token

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    readonly_fields = ('key',)
    list_display = ('user', 'key', 'created_at', 'expires_at', 'is_valid')
    search_fields = ('user__username', 'key')