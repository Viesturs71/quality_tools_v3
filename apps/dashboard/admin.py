from django.contrib import admin

from .models import UserPreference, UserWidgetPosition, Widget


class UserWidgetPositionInline(admin.TabularInline):
    model = UserWidgetPosition
    extra = 1


@admin.register(Widget)
class WidgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'widget_type', 'is_active')
    list_filter = ('widget_type', 'is_active')
    search_fields = ('name', 'description')


@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'theme', 'updated_at')
    list_filter = ('theme',)
    search_fields = ('user__username',)
    inlines = [UserWidgetPositionInline]
