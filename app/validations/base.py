import os
import re
from functools import wraps
from django.core.exceptions import ValidationError
from django.http import QueryDict
from django.utils.module_loading import import_string
from django.utils.translation import gettext_lazy as _
from datetime import date as datetime_date, datetime as datetime_datetime, timedelta as datetime_timedelta

from app.commons.helpers import is_numeric, is_valid_datetime, parse_body, parse_json, parse_request, to_jsonstr
from app.services.Core import Core

def __resolve_error_message(default_message, value, field, message, verbose_field):
    errormsg = message if message is not None else default_message
    if verbose_field is not None:
        value = verbose_field
    elif field is not None:
        value = field

    return (errormsg, value)

"""Decorator for injecting the input of request (form) into the rules function
"""
def input(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        # Do something before the function.
        data = {}
        if 'data' in kwargs:
            # dict type
            if isinstance(kwargs['data'], dict):
                data = kwargs['data']
            else: # tuple|list types
                for item in kwargs['data']:
                    if isinstance(item, dict) or isinstance(item, QueryDict):
                        data.update(item.dict())
        kwargs['data'] = data
        return fn(*args, **kwargs)
        # Do something after the function.
    return wrapper

@input
def required(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _required(value):
        if value == None or value == '':
            errormsg = message if message is not None else _('%(field)s is require.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _required

@input
def min(min_value, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _min(value):
        if value < min_value:
            errormsg = message if message is not None else _('%(field)s must be greater than %(min)s.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value, 'min': min_value })
    return _min

@input
def max(max_value, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _max(value):
        if value > max_value:
            errormsg = message if message is not None else _('%(field)s must be less than %(max)s.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value, 'max': max_value })
    return _max

@input
def before_date(date_value, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _before_date(value):
        _date = date_value
        # YYYY-MM-DD
        if re.search(r'^\d{4}-\d{1,2}-\d{1,2}$', _date) is not None:
            if (value > _date):
                errormsg = message if message is not None else _('%(field)s must be before %(date)s.')
                if verbose_field is not None:
                    value = verbose_field
                elif field is not None:
                    value = field
                raise ValidationError(errormsg, params={ 'field': value, 'date': _date })

        # {+-}{number}{weeks|days|hours|minutes|seconds|microseconds|milliseconds}
        format_updown = re.search(r'^(?P<sign>(\+|\-))(?P<num>\d+)\s+(?P<unit>(weeks|days|hours|minutes|seconds|microseconds|milliseconds))$', _date)
        if format_updown is not None:
            sign = format_updown['sign']
            num = format_updown['num']
            unit = format_updown['unit']
            num = -num if sign == '-' else num
            if unit == 'weeks': _date = datetime_date.today() + datetime_timedelta(weeks=num)
            elif unit == 'days': _date = datetime_date.today() + datetime_timedelta(days=num)
            elif unit == 'hours': _date = datetime_date.today() + datetime_timedelta(hours=num)
            elif unit == 'minutes': _date = datetime_date.today() + datetime_timedelta(minutes=num)
            elif unit == 'seconds': _date = datetime_date.today() + datetime_timedelta(seconds=num)
            elif unit == 'microseconds': _date = datetime_date.today() + datetime_timedelta(microseconds=num)
            elif unit == 'milliseconds': _date = datetime_date.today() + datetime_timedelta(milliseconds=num)
        elif _date == 'now':
            _date = datetime_date.today()
        elif _date == 'tomorrow':
            _date = datetime_date.today() + datetime_timedelta(days=1)
        elif _date == 'yesterday':
            _date = datetime_date.today() + datetime_timedelta(days=-1)
        else: # invalid format
            # Verify value as another field
            input_data = parse_request()['params']
            if date_value not in input_data:
                errormsg = message if message is not None else _('%(field)s is invalid date format.')
                if verbose_field is not None:
                    value = verbose_field
                elif field is not None:
                    value = field
                raise ValidationError(errormsg, params={ 'field': value, 'date': _date })

            another_value = input_data[date_value]
            _date = another_value
            value = input_data[field]

        if (value >= _date):
            errormsg = message if message is not None else _('%(field)s must be before %(date)s.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value, 'date': _date })

    return _before_date

@input
def after_date(date_value, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _after_date(value):
        _date = date_value
        now = datetime_date.today()
        # YYYY-MM-DD
        if re.search(r'^\d{4}-\d{1,2}-\d{1,2}$', _date) is not None:
            if (value < _date):
                errormsg = message if message is not None else _('%(field)s must be after %(date)s.')
                if verbose_field is not None:
                    value = verbose_field
                elif field is not None:
                    value = field
                raise ValidationError(errormsg, params={ 'field': value, 'date': _date })
            return None

        # {+-}{number}{weeks|days|hours|minutes|seconds|microseconds|milliseconds}
        format_updown = re.search(r'^(?P<sign>(\+|\-))(?P<num>\d+)\s+(?P<unit>(weeks|days|hours|minutes|seconds|microseconds|milliseconds))$', _date)
        if format_updown is not None:
            sign = format_updown['sign']
            num = format_updown['num']
            unit = format_updown['unit']
            num = -num if sign == '-' else num
            if unit == 'weeks': _date = now + datetime_timedelta(weeks=num)
            elif unit == 'days': _date = now + datetime_timedelta(days=num)
            elif unit == 'hours': _date = now + datetime_timedelta(hours=num)
            elif unit == 'minutes': _date = now + datetime_timedelta(minutes=num)
            elif unit == 'seconds': _date = now + datetime_timedelta(seconds=num)
            elif unit == 'microseconds': _date = now + datetime_timedelta(microseconds=num)
            elif unit == 'milliseconds': _date = now + datetime_timedelta(milliseconds=num)
        elif _date == 'now':
            _date = now
        elif _date == 'tomorrow':
            _date = now + datetime_timedelta(days=1)
        elif _date == 'yesterday':
            _date = now + datetime_timedelta(days=-1)
        else: # invalid format
            # Verify value as another field
            input_data = parse_request()['params']
            if date_value not in input_data:
                errormsg = message if message is not None else _('%(field)s is invalid date format.')
                if verbose_field is not None:
                    value = verbose_field
                elif field is not None:
                    value = field
                raise ValidationError(errormsg, params={ 'field': value, 'date': _date })

            another_value = input_data[date_value]
            _date = another_value
            value = input_data[field]

        if (value <= _date):
            errormsg = message if message is not None else _('%(field)s must be after %(date)s.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value, 'date': _date })

    return _after_date

@input
def between(min_value, max_value, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _between(value):
        # Validate value of `min`
        try:
            _min = float(min_value)
        except:
            errormsg = message if message is not None else _('Argument 1 [min] of rule [between] of %(field)s must be a number.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })

        # Validate value of `max`
        try:
            _max = float(max_value)
        except:
            errormsg = message if message is not None else _('Argument 2 [max] of rule [between] of %(field)s must be a number.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })

        if value < _min or value > _max:
            errormsg = message if message is not None else _('%(field)s must be between %(min)s and %(max)s.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value, 'min': min_value, 'max': max_value })
    return _between

@input
def between_date(start_date, end_date, field=None, message=None, verbose_field=None, data=None, **kwargs):
    start_date = start_date
    end_date = end_date
    def _between_date(value):
        # Validate start date
        split = start_date.split(':')
        start_date = split[0]
        start_date_format = '%Y-%m-%d'

        if len(split) > 1:
            start_date_format = split[1]

        if not is_valid_datetime(start_date, format=start_date_format):
            errormsg = _('Argument 1 [start_date] of rule [between_date] of %(field)s is invalid date or format.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })

        # Validate end date
        split = end_date.split(':')
        end_date = split[0]
        end_date_format = '%Y-%m-%d'

        if len(split) > 1:
            end_date_format = split[1]

        if not is_valid_datetime(end_date, format=end_date_format):
            errormsg = _('Argument 2 [end_date] of rule [between_date] of %(field)s is invalid date or format.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })

        # Validate date
        if value < start_date or value > end_date:
            errormsg, value = __resolve_error_message(_('%(field)s must be between %(start_date)s and %(end_date)s.'), value, field, message, verbose_field)
            raise ValidationError(errormsg, params={ 'field': value, 'start_date': start_date, 'end_date': end_date })
    return _between_date

@input
def email(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _email(value):
        pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        if not re.fullmatch(pattern, email):
            errormsg = message if message is not None else _('%(field)s is invalid email.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _email

@input
def date(*format, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _date(value):
        input_data = parse_request()
        value = input_data['params'][field]
        _format = '%Y-%m-%d'
        if len(format) > 0:
            _format = format[0]
        try:
            # Parse a date by specified format
            datetime_datetime.strptime(value, _format)
        except:
            errormsg = message if message is not None else _('%(field)s has invalid value or format.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _date

@input
def datetime(*format, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _datetime(value):
        _format = '%Y-%m-%d %H:%M:%S'
        if len(format) > 0:
            _format = format[0]
        try:
            # Parse a datetime by specified format
            datetime_datetime.strptime(value, _format)
        except:
            errormsg = message if message is not None else _('%(field)s has invalid datetime value or format.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _datetime

@input
def is_str(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_str(value):
        if not isinstance(value, str):
            errormsg = message if message is not None else _('%(field)s must be a string type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_str

@input
def is_dict(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_dict(value):
        if not isinstance(value, dict):
            errormsg = message if message is not None else _('%(field)s must be a dict type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_dict

@input
def is_tuple(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_tuple(value):
        if not isinstance(value, tuple):
            errormsg = message if message is not None else _('%(field)s must be a tuple type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_tuple

@input
def is_list(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_list(value):
        if not isinstance(value, list):
            errormsg = message if message is not None else _('%(field)s must be a list type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_list

@input
def is_int(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_int(value):
        if not isinstance(value, int):
            errormsg = message if message is not None else _('%(field)s must be a int type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_int

@input
def integer(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_integer(value):
        if not isinstance(value, int):
            errormsg = message if message is not None else _('%(field)s must be a int type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_integer

@input
def is_float(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_float(value):
        if not isinstance(value, float):
            errormsg = message if message is not None else _('%(field)s must be a float type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_float

@input
def is_complex(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_complex(value):
        if not isinstance(value, complex):
            errormsg = message if message is not None else _('%(field)s must be a complex type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_complex

@input
def is_range(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_range(value):
        if not isinstance(value, range):
            errormsg = message if message is not None else _('%(field)s must be a range type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_range

@input
def is_set(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_set(value):
        if not isinstance(value, set):
            errormsg = message if message is not None else _('%(field)s must be a set type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_set

@input
def is_frozenset(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_frozenset(value):
        if not isinstance(value, frozenset):
            errormsg = message if message is not None else _('%(field)s must be a frozenset type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_frozenset

@input
def is_bool(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_bool(value):
        if not isinstance(value, bool):
            errormsg = message if message is not None else _('%(field)s must be a bool type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_bool

@input
def is_bytes(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_frozenset(value):
        if not isinstance(value, bytes):
            errormsg = message if message is not None else _('%(field)s must be a bytes type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_frozenset

@input
def is_bytearray(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_bytearray(value):
        if not isinstance(value, bytearray):
            errormsg = message if message is not None else _('%(field)s must be a bytearray type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_bytearray

@input
def is_memoryview(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_memoryview(value):
        if not isinstance(value, memoryview):
            errormsg = message if message is not None else _('%(field)s must be a memoryview type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_memoryview

@input
def is_nonetype(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _is_nonetype(value):
        if not isinstance(value, NoneType):
            errormsg = message if message is not None else _('%(field)s must be a NoneType type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _is_nonetype

@input
def in_list(given_list, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _in_list(value):
        # Validate input parameter of the given list
        if not isinstance(given_list, list) and not isinstance(given_list, tuple):
            errormsg = _('Parameter of rule [in_list] for %(field)s must be a list or tuple type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field

            raise ValidationError(errormsg, params={ 'field': value })
        # If it is not in the given list
        if value not in given_list:
            errormsg = message if message is not None else _('%(field)s must be in list (%(given_list)s).')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field

            raise ValidationError(errormsg, params={ 'field': value, 'given_list': ','.join(given_list) })
    return _in_list

@input
def not_in(given_list, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _not_in(value):
        # Validate input parameter of the given list
        if not isinstance(given_list, list) and not isinstance(given_list, tuple):
            errormsg = _('Parameter of rule [not_in] for %(field)s must be a list or tuple type.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field

            raise ValidationError(errormsg, params={ 'field': value })
        # If it is in the given list
        if value in given_list:
            errormsg = message if message is not None else _('%(field)s must not be in list (%(given_list)s).')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field

            raise ValidationError(errormsg, params={ 'field': value, 'given_list': ','.join(given_list) })
    return _not_in

@input
def numeric(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _numeric(value):
        if not is_numeric(value):
            errormsg = message if message is not None else _('%(field)s must be a numeric.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _numeric

@input
def file(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _file(value):
        if isinstance(value, str):
            if not os.path.exists(value):
                errormsg = message if message is not None else _('%(field)s must be an existing file.')
                if verbose_field is not None:
                    value = verbose_field
                elif field is not None:
                    value = field
                raise ValidationError(errormsg, params={ 'field': value })
    return _file

@input
def required_if(another_field, field=None, message=None, verbose_field=None, verbose_another_field=None, data=None, **kwargs):
    def _required_if(value):
        # Validate field
        if not field:
            errormsg = _('Missing argument 2 [field] of rule [required_if] for %(field)s.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })

        input_data = parse_request()['params']
        # Validate input
        if not input_data:
            errormsg = _('Input of rule [required_if] of %(field)s is empty.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })

        # Validate specified antoher field
        if not another_field or another_field not in input_data:
            errormsg = message if message is not None else _('Key [%(another_field)s] not exist.')
            raise ValidationError(errormsg, params={ 'another_field': another_field })

        if not input_data[another_field]:
            errormsg = message if message is not None else _('%(another_field)s is empty.')
            if verbose_another_field is not None:
                value = verbose_another_field
            elif another_field is not None:
                value = another_field
            raise ValidationError(errormsg, params={ 'another_field': value })
    return _required_if

@input
def alpha(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _alpha(value):
        if not re.search(r'^[a-zA-Z\s]+$', value, re.IGNORECASE):
            errormsg = message if message is not None else _('%(field)s contains only spaces and alphabets.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _alpha

@input
def alpha_dash(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _alpha_dash(value):
        if not re.search(r'^[a-zA-Z\s_-]+$', value, re.IGNORECASE):
            errormsg = message if message is not None else _('%(field)s contains only spaces, dashes (_, -) and alphabets.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _alpha_dash

@input
def alpha_numeric(field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _alpha_numeric(value):
        if not re.search(r'^[0-9a-zA-Z\s]+$', value, re.IGNORECASE):
            errormsg = message if message is not None else _('%(field)s contains only spaces, digits and alphabets.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value })
    return _alpha_numeric

@input
def size(num, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _size(value):
        if len(value) != int(num):
            errormsg = message if message is not None else _('Size of %(field)s must be %(num)s.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field
            raise ValidationError(errormsg, params={ 'field': value, 'num': num })
    return _size

@input
def unique(model, column, id, field=None, message=None, verbose_field=None, data=None, **kwargs):
    def _unique(value):
        try:
            _model = model
            if isinstance(_model, str):
                _model = import_string(_model)

            result = _model.objects.filter(**{column:value}).exclude(pk=id)

            if result.count() > 0:
                errormsg = message if message is not None else _('%(field)s must be unique.')
                if verbose_field is not None:
                    value = verbose_field
                elif field is not None:
                    value = field
                raise ValidationError(errormsg, params={ 'field': value })
        except _model.DoesNotExist:
            pass
    return _unique

@input
def color_hex(field=None, both=False, message=None, verbose_field=None, data=None, **kwargs):
    def _color_hex(value):
        value = str(value)
        pattern = r'^#([a-fA-F0-9]{6}|[a-fA-F0-9]{3})$' if both else r'^#[a-fA-F0-9]{6}$'
        if not re.match(pattern, value, re.I):
            errormsg = message if message is not None else _('%(field)s has invalid hex code.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field

            raise ValidationError(errormsg, params={ 'field': value })
    return _color_hex

@input
def color_hex3(field=None, both=True, message=None, verbose_field=None, data=None, **kwargs):
    def _color_hex3(value):
        value = str(value)
        if not re.match(r'^#[a-fA-F0-9]{3}$', value, re.I):
            errormsg = message if message is not None else _('%(field)s has invalid hex code.')
            if verbose_field is not None:
                value = verbose_field
            elif field is not None:
                value = field

            raise ValidationError(errormsg, params={ 'field': value })
    return _color_hex3

@input
def rules(_rules, field=None, messages=None, verbose_field=None, data=None, **kwargs):
    """ Build an array of given rules

        Usage:
            rules('even|min:10|between:25,20', field='first_name', verbose_field='First name', data=args, messages={
                <rule1>: <messages1>,
                <rule2>: <messages2>,
                <rule3>: <messages3>,
            })
    """
    _rules = str(_rules).split('|')
    out = []
    for rule in _rules:
        split = str(rule).split(':')
        rule = split.pop(0)
        args = ''
        # Resolve arguments
        if len(split) > 0: # Arguments required
            message = None

            # Verify types of argument values are string or tuple
            if not re.search(r'^\(.*\)$', split[0], re.IGNORECASE):
                # Add '' to each values of parameters if it is a string
                _args = split[0].split(',')
                split[0] = ','.join(map(lambda x : f"'{x}'" if isinstance(x, str) else x, _args))

            args += ','.join(split)

        # Error message
        if isinstance(messages, dict) and rule in messages:
            message = messages[rule]
            args += f",message='{message}'"

        # Verbose field
        if verbose_field is not None:
            args += f",verbose_field='{verbose_field}'"

        # Field
        if field is not None:
            args += f",field='{field}'"

        # Input data (get, post, files)
        if data:
            args += f",data={str(data)}"

        # More arguments
        if kwargs:
            for key, value in kwargs.items():
                args += f",{key}='{value}'"

        args = args.strip(',')

        out.append(eval(f"{rule}({args})"))
    return out
