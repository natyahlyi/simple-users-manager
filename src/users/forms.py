import re
from django import forms
from django.core.validators import EMPTY_VALUES


ua_phone_regex = re.compile(r'^(\+380)?\d{9}$')


class UAPhoneNumberField(forms.CharField):
    default_error_messages = {
        'invalid': "Phone number must be in the format: +380987654321.",
    }

    def clean(self, value):
        super(UAPhoneNumberField, self).clean(value)
        if value in EMPTY_VALUES:
            return u''
        match = ua_phone_regex.match(value)
        if match:
            return value
        raise forms.ValidationError(self.error_messages['invalid'])


class AlphabeticCharFiled(forms.CharField):
    default_error_messages = {
        'invalid': "Only alphanumeric characters are allowed.",
    }

    def clean(self, value):
        super(AlphabeticCharFiled, self).clean(value)
        words = value.split(' ')
        for word in words:
            if not word.isalpha():
                raise forms.ValidationError(self.error_messages['invalid'])
        return value


class CreateUserForm(forms.Form):
    name = AlphabeticCharFiled(max_length=64, required=True)
    email = forms.EmailField(max_length=128, required=True)

    phone = UAPhoneNumberField(required=False)
    mobile = UAPhoneNumberField(required=False)

    status = forms.ChoiceField(choices=[('Active', 'Active'),
                                        ('Inactive', 'Inactive')],
                               required=False)


class UpdateUserForm(CreateUserForm):
    memberships = forms.CharField(required=False)

    def clean_memberships(self):
        memberships = self.cleaned_data.get('memberships', '').split('/')
        return [int(course) for course in memberships if course]
