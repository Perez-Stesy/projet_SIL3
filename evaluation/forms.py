from django import forms
from .models import Evaluation

class EvaluationForm(forms.ModelForm):
    class Meta:
        model=Evaluation
        fields= ['note', 'commentaire']
        widgets={'commentaire': forms.Textarea(attrs={'rows':4}),}

        