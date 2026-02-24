import urllib.parse

from django import template
register = template.Library()

@register.simple_tag(takes_context=True)
def query_keeper(context, key, value):
    dict_ = context['request'].GET.copy()
    dict_[key] = value
    return "?" + urllib.parse.urlencode(dict_)