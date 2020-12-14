from django import forms
from .models import Hanke


class HankeDetailForm(forms.ModelForm):
    class Meta:
        model = Hanke
        fields = [
            'nimi',
            'tyyppi',
        ]


