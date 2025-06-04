from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def split(value, arg):
    """
    Split a string into a list on the specified delimiter.
    Usage: {{ value|split:"delimiter" }}
    """
    return value.split(arg)
