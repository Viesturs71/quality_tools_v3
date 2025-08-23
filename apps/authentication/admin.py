from django.contrib import admin
from .models.token import Token
from .models.one_time_password import OneTimePassword


@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('user', 'key_preview', 'created_at', 'expires_at', 'is_valid')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'user__email', 'key')
    date_hierarchy = 'created_at'
    readonly_fields = ('key', 'created_at')
    
    def key_preview(self, obj):
        return f"{obj.key[:10]}..."
    
    key_preview.short_description = 'Key'


@admin.register(OneTimePassword)
class OneTimePasswordAdmin(admin.ModelAdmin):
    list_display = ('user', 'code', 'created_at', 'expires_at', 'is_used', 'is_valid')
    list_filter = ('is_used', 'created_at')
    search_fields = ('user__username', 'user__email')
    date_hierarchy = 'created_at'
    readonly_fields = ('code', 'created_at', 'expires_at')
    
    def is_valid(self, obj):
        return obj.is_valid()
    
    is_valid.boolean = True
    is_valid.short_description = 'Valid'
