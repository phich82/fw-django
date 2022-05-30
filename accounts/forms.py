from django import forms

from app.validations.rules import before_date, datetime, date, min, max, required, rules


class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)

    name = forms.CharField(
        label='Name',
        help_text='Enter your name',
        # Add attributes to elements via widget
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages = {
            'invalid': 'Name is invalid.',
            'required': 'Name is required xxx.'
        },
        validators=rules('required|required_if:"age"|not_in:("1","2","3")|size:4|color_hex3', field='name', verbose_field='Name', verbose_another_field='Age', messages={
            'is_int': 'It must be an integer.',
        }),
        # validators=[required(field='name', verbose_field='Name')],
        required=True
    )
    age = forms.FloatField(
        label='Age',
        help_text='Enter your age',
        # Add attributes to elements via widget
        widget=forms.NumberInput(attrs={'class': 'form-control'}),
        validators=[
            # min(10, verbose_field='Age field', message='It must be greater than %s.' % 10),
            max(30, verbose_field='Age field'),
        ],
        error_messages = {
            'invalid': 'Age is required.',
            'required': ''
        },
    )
    date = forms.DateField(
        required=False,
        disabled=False,
        initial='',
        label='Start Date',
        help_text='Enter state date',
        # Add attributes to elements via widget
        widget=forms.DateInput(
            format='%d-%m-%Y',
            attrs={
                'class': 'form-control datepicker',
                'placeholder': 'DD-MM-YYYY',
                'type': "text"
            }
        ),
        validators=[
            date('%d-%m-%Y', verbose_field='Start date'),
            # before_date('now', verbose_field='Start date')
        ],
        error_messages = {
            'invalid': 'Date format is invalid.',
            'required': 'Date is required.'
        },
        # Date format for input
        input_formats=['%d-%m-%Y']
    )
