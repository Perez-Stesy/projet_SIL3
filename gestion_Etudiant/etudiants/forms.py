from django import forms
from .models import Etudiant, Promotion


class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = ['promotion', 'nom', 'prenom', 'numero_etudiant', 'email', 
                  'date_naissance', 'moyenne_generale']
        widgets = {
            'promotion': forms.Select(attrs={
                'class': 'form-select',
                'id': 'promotion-select'
            }),
            'nom': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Entrez le nom'
            }),
            'prenom': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Entrez le prénom'
            }),
            'numero_etudiant': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Numéro étudiant unique'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-input',
                'placeholder': 'email@exemple.com'
            }),
            'date_naissance': forms.DateInput(attrs={
                'class': 'form-input',
                'type': 'date'
            }),
            'moyenne_generale': forms.NumberInput(attrs={
                'class': 'form-input',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
                'max': '20'
            })
        }
        labels = {
            'promotion': 'Promotion',
            'nom': 'Nom',
            'prenom': 'Prénom',
            'numero_etudiant': 'Numéro étudiant',
            'email': 'Email',
            'date_naissance': 'Date de naissance',
            'moyenne_generale': 'Moyenne générale'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['promotion'].queryset = Promotion.objects.all().order_by('-annee', 'nom')

