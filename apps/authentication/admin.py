from django.contrib import admin
from .models import Token, OneTimePassword


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key_preview', 'created_at', 'expires_at', 'is_valid_display')
    list_filter = ('created_at', 'expires_at')
    search_fields = ('user__username', 'user__email', 'key')
    date_hierarchy = 'created_at'
    
    def key_preview(self, obj):
        return f"{obj.key[:10]}..."
    
    def is_valid_display(self, obj):
        return obj.is_valid
    
    key_preview.short_description = 'Key'
    is_valid_display.short_description = 'Is Valid'
    is_valid_display.boolean = True


@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_used')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created_at'
    readonly_fields = ('code',)
