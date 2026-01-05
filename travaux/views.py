from django.shortcuts import render, redirect
from .forms import TravailForm
from django.contrib.auth.decorators import login_required, user_passes_test

# Create your views here.

#def is_formateur(user):
 #   return user.groups.filter(name='Formateur').exists()

#@login_required
#@user_passes_test(is_formateur)

def creer_travail(request):
    form=TravailForm()
    if request.method == 'POST':
        form=TravailForm(request.POST)
        if form.is_valid():
            travail=form.save(commit=False)
            travail.formateur = request.user
            travail.save()
            return redirect('travail_success')
        
    return render(request, 'travaux/creer_travail.html',{'form':form})
        
def travail_success(request):
    return render(request, 'travaux/success.html')
