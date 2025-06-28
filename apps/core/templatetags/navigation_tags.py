from django import template
from django.conf import settings

register = template.Library()

@register.inclusion_tag('users/includes/user_navigation.html', takes_context=True)
def render_navigation(context):
    user = context['request'].user
    NAVIGATION_APPS = getattr(settings, 'NAVIGATION_APPS', {})
    def filter_navigation_by_permissions(apps, user):
        if user.is_superuser:
            return [{'name': app, **data} for app, data in apps.items()]
        allowed = []
        for app, data in apps.items():
            if any(user.has_perm(f"{app}.{perm}") for perm in data.get('permissions', [])):
                allowed.append({'name': app, **data})
        return allowed

    apps = filter_navigation_by_permissions(NAVIGATION_APPS, user)
    return {'apps': apps}
