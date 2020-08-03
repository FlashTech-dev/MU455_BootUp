from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Sentiment

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email']

CHOICES=[('Text','File'),
         ('File','Text')]

class SentimentForm(forms.Form):
    text = forms.CharField(required=False)
    docfile = forms.FileField(
        label='Select a file',
        required=False
    )
    value = forms.ChoiceField(choices=CHOICES, widget = forms.RadioSelect)