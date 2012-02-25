from django import forms
from django.contrib.auth.forms import UserCreationForm


class RegistrationForm(UserCreationForm):
    code = forms.CharField(
        help_text='Enter the code provided to you on your invitation response card. Case insensitive.',
        max_length=11,
    )