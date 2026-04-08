from django import template
from django.utils.safestring import mark_safe
from django.conf import settings
import os

register = template.Library()

@register.simple_tag
def inline_svg(path):
    # Cari di semua STATICFILES_DIRS
    for static_dir in settings.STATICFILES_DIRS:
        full_path = os.path.join(static_dir, path)
        if os.path.exists(full_path):
            with open(full_path, 'r') as f:
                return mark_safe(f.read())
    return ''