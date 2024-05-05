import logging
import re

from django.core.validators import ValidationError, EmailValidator
from django import forms


def validate_phone(number):
    if re.match(r'^\+\d{3} \(\d{2}\) \d{3}-\d{2}-\d{2}$', number):
        logging.log(1, 'mama')
        return number
    else:
        raise ValidationError("Phone must be in format +375 (XX) XXX-XX-XX")


class RegistrationForm(forms.Form):
    name = forms.CharField(min_length=1, max_length=20, label='Имя', required=True)
    surname = forms.CharField(min_length=1, max_length=40, label='Фамилия', required=True)
    second_name = forms.CharField(min_length=2, max_length=40, label='Отчество', required=True)
    age = forms.IntegerField(min_value=18, max_value=111, label="Ваш возраст",required=True)
    phone_number = forms.CharField(min_length=15, max_length=30, label="Ваш телефон", validators=[validate_phone], required=True)
    address = forms.CharField(max_length=100, label='Домашний адресс', required=True)
    email = forms.EmailField(validators=[EmailValidator], required=True)
    login = forms.CharField(min_length=5, max_length=30, label="Ваш логин", required=True)
    password = forms.CharField(widget=forms.PasswordInput())
    password_confirm = forms.CharField(widget=forms.PasswordInput())

    def clean_age(self):
        data = self.cleaned_data['age']
        data = int(data)
        if data < 18:
            raise forms.ValidationError("You must be older than 18")
        return data


class LoginForm(forms.Form):
    login = forms.CharField(min_length=5, max_length=30, label="Ваш логин")
    password = forms.CharField(widget=forms.PasswordInput())
