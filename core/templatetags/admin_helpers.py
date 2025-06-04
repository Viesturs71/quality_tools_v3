from django import template
from django.urls import reverse, NoReverseMatch

register = template.Library()

@register.filter
def has_perm(perm_string, user):
    """Check if user has the specified permission"""
    return user.has_perm(perm_string)

@register.filter
def admin_url_exists(url_pattern):
    """Check if an admin URL pattern exists"""
    try:
        reverse(url_pattern)
        return True
    except NoReverseMatch:
        return False
