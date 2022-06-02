"""
Register custom tags here

"""
import copy
import datetime
from django import template
from django.http import QueryDict
from app.commons.helpers import trans as translate

from app.settings.base import BASE_DIR

register = template.Library()

@register.inclusion_tag('app/style.html')
def includecss(style_paths):
    """Include *.css file

    Args:
        style_path (str): each css file path is separated together by comma (,)

    Returns:
        dict
    """
    if not isinstance(style_paths, tuple) and not isinstance(style_paths, list):
        style_paths = style_paths.split(',')

    return { 'style_paths': style_paths }

@register.inclusion_tag('app/style.html')
def importcss(style_path):
    """Alias of `includecss` function
    """
    return includecss(style_path)

@register.inclusion_tag('app/style.html')
def css(style_path):
    """Alias of `includecss` function
    """
    return includecss(style_path)

@register.inclusion_tag('app/style.html')
def importcsslib(lib):
    if lib == 'spectrum':
        return includecss('css/libs/spectrum.min.css')
    elif lib == 'datetimepicker':
        return includecss('css/libs/bootstrap-datetimepicker.min.css')
    return ''

@register.inclusion_tag('app/script.html')
def includejs(js_paths):
    """Include the *.js files

    Args:
        js_paths (str): each js file path is separated by comma (,)

    Returns:
        list
    """
    if isinstance(js_paths, str):
        js_paths = list(map(lambda path: path.strip(), js_paths.split(',')))

    return { 'js_paths': js_paths }

@register.inclusion_tag('app/script.html')
def importjs(js_path):
    return includejs(js_path)

@register.inclusion_tag('app/script.html')
def js(js_path):
    return includejs(js_path)

@register.inclusion_tag('app/script.html')
def importlib(lib):
    if lib == 'datetimepicker':
        return includejs('js/libs/bootstrap-datetimepicker.min.js')
    elif lib == 'spectrum':
        return includejs('js/libs/spectrum.min.js')
    elif lib == 'moment':
        return includejs('js/libs/moment-with-locales.min.js')
    return ''

@register.inclusion_tag('pagination.html', takes_context=True)
def pagination_links(context):
    context = copy.copy(context)
    return context

@register.inclusion_tag('app/error.html', takes_context=True)
def error(context, field):
    errors = context.get('form').errors
    has_error = field in errors
    error = errors.get(field)[0] if has_error else ''
    return {
        'has_error': has_error,
        'error': error
    }

@register.simple_tag
def query_string(*args, **kwargs):
    """ Builds an encoded URL query string from dictionaries of query parameters and individual query parameters.

        Args:
            args: tuple<QueryDict>
            kwargs: dict
        Returns:
            str
    """
    query_dict = QueryDict(mutable=True)

    # Verify dict parameters of tuple arguments (*args)
    for arg in args:
        if isinstance(arg, QueryDict):
            query_dict.update(arg)

    # Track keys with none values
    remove_keys = []

    # Verify dict arguments (**kwargs)
    for k, v in kwargs.items():
        if v is None:
            remove_keys.append(k)
        elif isinstance(v, list):
            query_dict.setlist(k, v)
        else:
            query_dict[k] = v

    # Remove keys with none values
    for k in remove_keys:
        if k in query_dict:
            del query_dict[k]

    qs = query_dict.urlencode()

    return '?' + qs if qs else ''

@register.simple_tag
def current_time(format_string):
    return datetime.datetime.now().strftime(format_string)

@register.simple_tag
def trans(key, lang='en', options={}):
    return translate(key, lang=lang, options=options)

@register.simple_tag
def __(key, lang='en', options={}):
    return translate(key, lang=lang, options=options)

@register.simple_tag
def t(key, lang='en', options={}):
    return translate(key, lang=lang, options=options)

@register.simple_tag
def my_tag(a, b, *args, **kwargs):
    """ _summary_

        {% my_tag 123 "abcd" book.title warning=message|lower profile=user.profile %}

    Returns:
        mixed
    """

    print({*args}, {**kwargs})

    warning = kwargs['warning']
    profile = kwargs['profile']

    return warning + profile

