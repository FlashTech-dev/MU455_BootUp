from django import forms

from .models import Sentiment

class predict(forms.ModelForm):

    class Meta:
        model = Sentiment