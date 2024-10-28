# templatetags/star_filters.py

from django import template

register = template.Library()

@register.filter
def star_range(value):
    return range(1, 6)  # Returns a range from 1 to 5 (inclusive)
