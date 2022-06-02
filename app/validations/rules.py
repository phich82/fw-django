from .base import *

@input
def after(date_value, field=None, message=None, verbose_field=None, data=None, **kwargs):
    """ Alias of after_date function """
    return after_date(date_value, field=field, message=message, verbose_field=verbose_field, data=data, **kwargs)
