from django import template

from bugs.models import Bug

register = template.Library()

@register.simple_tag
def count_bugs():
    return Bug.objects.count()