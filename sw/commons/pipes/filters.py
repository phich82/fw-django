"""
Register custom filters (pipes) here

"""

from django import template

from sw.commons.helpers import normalize as _normalize

register = template.Library()

""" Use decorator

    Notes: Django is ONLY allow to pass ONE argument to function,

    Returns:
        string
"""
# @register.filter(name='cut') # filter name (cut)
@register.filter # default filter name is function name bellow (cut)
def replace(value, argument):
    args = argument.split(',')
    if (len(args) < 2):
        raise Exception(f"Filter [replace] need two arguments.")
    return value.replace(args[0].strip(), args[1])

@register.filter
def normalize(num):
    return _normalize(num)
