from django import forms
from .models import Travail

class TravailForm(forms.ModelForm):
    class Meta:
        model = Travail
        fields = ['titre', 'consigne', 'type']