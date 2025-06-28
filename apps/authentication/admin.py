from django.contrib import admin
from .models import Token, OneTimePassword


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key_preview', 'created', 'expires', 'is_active')
    list_filter = ('is_active', 'created')
    search_fields = ('user__username', 'user__email', 'key')
    date_hierarchy = 'created'
    
    def key_preview(self, obj):
        return f"{obj.key[:10]}..."
    
    key_preview.short_description = 'Key'


@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created_at'
    readonly_fields = ('code',)
