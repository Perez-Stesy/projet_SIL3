from django.shortcuts import render, redirect

# Create your views here.
from django.contrib.auth.models import Group
from django.contrib import messages

from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import FormateurCreationForm

from django.core.mail import send_mail
from django.conf import settings

# Vérifie que l’utilisateur est Directeur
#def is_directeur(user):
 #  return user.groups.filter(name='Directeur').exists()

#@login_required
#@user_passes_test(is_directeur, login_url='/login/')
def creer_formateur(request):
    if request.method == 'POST':
        form = FormateurCreationForm(request.POST)
        if form.is_valid():
            formateur = form.save()
            recipient_email = form.cleaned_data.get('email')
            send_mail('Compte formateur crée', f'Bonjour{formateur.username}, votre compte a été créé avec succès', settings.EMAIL_HOST_USER, [recipient_email], fail_silently=False,)
            messages.success(request, "Formateur créé avec succès.")
            return redirect('creer_formateur')  # redirige après création
    else:
        form = FormateurCreationForm()
    return render(request, 'users/creer_formateur.html', {'form': form})


