from unicodedata import numeric
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.utils.deconstruct import deconstructible
from django.core.validators import RegexValidator



# These values, if given to validate(), will trigger the self.required check.
EMPTY_VALUES = (None, "", [], (), {})

@deconstructible
class Min:
    # message = _('%(value)s must be at least %(min)s.'),
    field = '%(field)s'
    message = '%(value)s must be at least %(min)s.'
    attribute = '%(attribute)s'
    code = None

    def __init__(self, min, field=None, message=None, attribute=None, code=None):
        if min is not None:
            self.min = min
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code
        if self.min and (type(self.min) != int and type(self.min) != float):
            print(self.min, type(self.min))
            raise TypeError( "it must be a numeric.")

    def __call__(self, value):
        """
        Validate input
        """
        if value < self.min:
            # raise ValidationError(self.message, code=self.code, params={"value": value, "num": self.min})
            raise ValidationError(self.message, code=self.code, params={'value': 'Field', 'min': self.min})

    def __eq__(self, other):
        return (
            isinstance(other, Min)
            and (self.message == other.message)
            and (self.code == other.code)
        )
min = lambda min, field=None, message=None, attribute=None, code=None: Min(min);

@deconstructible
class Between:
    # message = _('%(value)s must be at least %(num)s.'),
    message = "%(value)s must be between %(min)s and %(max)s.",
    code = "invalid"
    def __init__(self, min, max, message=None, code=None):
        self.min = min
        self.max = max
        if message is not None:
            self.message = message
        if code is not None:
            self.code = code

        if self.min and (isinstance(self.min, str) and not self.min.isnumeric()):
            raise TypeError( "Argument [min] must be a numeric.")

        if self.max and (isinstance(self.max, str) and not self.max.isnumeric()):
            raise TypeError( "Argument [max] must be a numeric.")

        if float(self.min) > float(self.max):
            raise TypeError( "Argument [min] must be less than argument [max].")

    def __call__(self, value):
        """
        Validate input
        """
        if value < float(self.min) or value > float(self.max):
            # raise ValidationError(self.message, code=self.code, params={"value": value, "num": self.min})
            raise ValidationError(self.message, code=self.code)

    def __eq__(self, other):
        return (
            isinstance(other, Between)
            and (self.message == other.message)
            and (self.code == other.code)
        )
between = lambda min, max: Between(min, max);

# def min(value, n = 0):
#     if (len(value) > n):
#         raise ValidationError(
#             _('%(value)s must be at least %(num)s.'),
#             params={'value': value, 'num': n},
#         )

def max(value, n = 0):
    if (len(value) < n):
        raise ValidationError(
            _('%(value)s must be maximum as %(num)s.'),
            params={'value': value, 'num': n},
        )

def even(value):
    if value % 2 != 0:
        raise ValidationError(
            _('%(value)s is not an even number.'),
            params={'value': value},
        )

def rules(_rules, field = None, messages = [], attributes = []):
    _rules = str(_rules).split('|')
    out = []
    for rule in _rules:
        split = str(rule).split(':')
        rule = split[0]
        if len(split) > 1:
            split.pop(0)
            print(split)
            args = ','.join(map(lambda x : str(x), split))
            out.append(eval(f"{rule}({args})"))
        else:
            out.append(eval(rule))
    return out

#o = rules('even|min:10|between:25,20')
#print(o[2](9))
