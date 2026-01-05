from django import forms
from django.contrib.auth.models import User, Group

from .models import Formateur

class FormateurCreationForm(forms.Form):
    username= forms.CharField(label="Nom utilisateur")
    last_name= forms.CharField(label="Nom")
    first_name= forms.CharField(label="Prenom")
    email= forms.EmailField(label="Email")
    specialite= forms.CharField(label="Spécialité")
   

    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Ce nom utilisateur existe deja")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Cette adresse email existe deja")
        return email

    def save(self):
        import random
        import string
        password=''.join(random.choices(string.ascii_letters + string.digits, k=12))


        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            password=password,
            email=self.cleaned_data['email'],
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],

            
        )

        formateur = Formateur.objects.create(
            user=user,
            specialite=self.cleaned_data['specialite']
            
      
            
        )
       
        group, created = Group.objects.get_or_create(name='formateur')
        user.groups.add(group)

        return formateur