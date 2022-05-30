import json
import re
from django.core import serializers
from datetime import datetime as datetime
from django.utils.translation import gettext
from django.utils import translation

from app.commons.constant import SUPPORTED_LANGUAGES

from app.services.Core import Core

def function_exists(name): return name in globals()

if not function_exists('parse_request'):
    def parse_request(request=None):
        params = {}
        query_params = {}
        files = None
        request = request if request else Core.request
        if request:
            files = request.FILES
            for key in request.POST:
                params[key] = request.POST.get(key)
            for key in request.GET:
                query_params[key] = request.GET.get(key)
        return {
            'params': params,
            'query_params': query_params,
            'files': files,
        }

if not function_exists('parse_body'):
    def parse_body(request):
        try:
            return json.load(request)
        except Exception as e:
            # Track error here: str(e)
            print(str(e))
            return False

if not function_exists('parse_json'):
    def parse_json(input, key=None):
        try:
            data = json.loads(serializers.serialize('json', input))
            if isinstance(key, str) and key:
                data = [r[key] for r in data]
            return data
        except Exception as e:
            # Track error here: str(e)
            return False

if not function_exists('json_encode'):
    def json_encode(params):
        if isinstance(params, str) or isinstance(params, dict) or isinstance(params, list) or isinstance(params, tuple):
            return json.dumps(params, indent = 4)
        return str(params)

if not function_exists('to_jsonstr'):
    def to_jsonstr(input, key=None):
        print('xx => ', input)
        json = parse_json(input, key=key)
        if json is False:
            return False
        return str(json)

if not function_exists('is_valid_datetime'):
    def is_valid_datetime(date_value, format='%Y-%m-%d'):
        try:
            datetime.strptime(date_value, format)
            return True
        except:
            return False

if not function_exists('is_numeric'):
    def is_numeric(s):
        try:
            n = str(float(s))
            if n == "nan" or n == "inf" or n == "-inf" :
                return False
        except Exception:
            try:
                complex(s) # for complex
            except ValueError:
                return False
        return True

if not function_exists('normalize'):
    """ Remove .0000000... from number"""
    def normalize(n):
        if not is_numeric(n):
            return n
        parts = str(n).split('.')
        if len(parts) > 1 and int(parts[1]) == 0:
            n = int(parts[0])
        return n

if not function_exists('trans'):
    def trans(key, lang='en', options={}):
        if not key:
            return f'Missing `key` argument.'

        if isinstance(lang, dict):
            options = lang
            lang = 'en'

        if not isinstance(options, dict):
            options = {}

        if lang not in SUPPORTED_LANGUAGES:
            return f'Language `{lang}` not supported.'

        translations = __import__(f'app.lang.{lang}.translations', fromlist=[f'app.lang.{lang}']).translations

        value = None
        is_first = True
        tracked_keys = ''

        for k in key.split('.'):
            tracked_keys += f'.{k}' if tracked_keys else k
            if is_first:
                if k not in translations:
                    if k not in translations['common']:
                        return f'Key [{tracked_keys}] not exists.'
                    else:
                        value = translations['common'][k]
                else:
                    value = translations[k]
                is_first = False
            else:
                if k not in value:
                    return f'Key [{tracked_keys}] not exists.'
                value = value[k]

        if not isinstance(value, str):
            return f'Value of key [{tracked_keys}] should be a string: {str(value)}'

        for k in options:
            value = re.sub('{{'+k+'}}', str(options[k]), value)

        return value

if not function_exists('_'):
    def _(message):
        return gettext(message)

if not function_exists('set_lang'):
    def set_lang(lang):
        translation.activate(lang)

if not function_exists('get_lang'):
    def get_lang(lang):
        return translation.get_language()

def __(key, lang='en', options={}):
    return trans(key, lang=lang, options=options)

def t(key, lang='en', options={}):
    return trans(key, lang=lang, options=options)
