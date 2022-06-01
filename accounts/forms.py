from django import forms
from accounts.models import Account

from app.validations.rules import before_date, between, datetime, date, min, max, required, rules

class AccountForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(AccountForm, self).__init__(*args, **kwargs)

        self.fields['name'].validators = []

    name = forms.CharField(
        required=True,
        label='Name',
        help_text='Enter your name',
        # Add attributes to elements via widget
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages = {
            'invalid': 'Name is invalid.',
            'required': 'Name is required xxx.'
        },
        validators=rules('required|required_if:"age"|not_in:("1","2","3")|size:4|color_hex3',
            field='name', verbose_field='Name', verbose_another_field='Age',
            messages={
                'is_int': 'It must be an integer.',
            }
        )
    )

class TestForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(TestForm, self).__init__(*args, **kwargs)

        # Add new more rules to validators
        self.fields['name'].validators.append(
            rules('unique:"accounts.models.Account","name",1', field='name', verbose_field='Name')[0]
        )

    name = forms.CharField(
        required=True,
        label='Name',
        help_text='Enter your name',
        # Add attributes to elements via widget
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        error_messages = {
            'invalid': 'Name is invalid.',
            'required': 'Name is required xxx.'
        },
        validators=rules('required|required_if:"age"|not_in:("1","2","3")|size:7',
            field='name', verbose_field='Name', verbose_another_field='Age',
            messages={
                'is_int': 'It must be an integer.',
            }
        )
    )

    age = forms.FloatField(
        required=True,
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

    start_date = forms.DateTimeField(
        required=True,
        label='Start date',
        help_text='Enter your start date',
        input_formats=['%d/%m/%Y %H:%M'],
        widget=forms.DateTimeInput(
            format='%d/%m/%Y %H:%M',
            attrs={
                'class': 'form-control',
                'name': 'start_date',
                'id': 'start_date',
                'placeholder': 'DD/MM/YYYY',
            }
        ),
        validators=[
            date('%d/%m/%Y', verbose_field='Start date'),
            # before_date('now', verbose_field='Start date')
        ],
        error_messages = {
            'invalid': 'Start date format is invalid.',
            'required': 'Start date is required.'
        }
    )

    end_date = forms.DateTimeField(
        required=False,
        disabled=False,
        initial='',
        label='End Date',
        help_text='Enter end date',
        # Date format for input
        input_formats=['%d/%m/%Y'],
        # Add attributes to elements via widget
        widget=forms.DateTimeInput(
            format='%d/%m/%Y',
            attrs={
                'class': 'form-control datepicker',
                'placeholder': 'DD/MM/YYYY',
                # 'type': "text",
                'name': 'end_date',
                'id': 'end_date'
            }
        ),
        validators=[
            date('%d/%m/%Y', verbose_field='End date'),
            # before_date('now', verbose_field='Start date')
        ],
        error_messages = {
            'invalid': 'End date format is invalid.',
            'required': 'End date is required.'
        }
    )
