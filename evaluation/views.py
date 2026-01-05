from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Travail
from .forms import EvaluationForm

# Create your views here.

#@login_required
def evaluer_travail(request, travail_id):
    travail=get_object_or_404(Travail, id=travail_id)
    if request.method == 'POST':
        form =EvaluationForm(request.POST)
        if form.is_valid():
            evaluation=form.save(commit=False)
            evaluation.travail=travail
            evaluation.formateur=request.user
            evaluation.save()

            return redirect('evaluation_success')
            
        else:
            form = EvaluationForm()

    return render(request, 'evaluation/evaluer_travail.html', {'form': form, 'travail':travail})
   

def evaluation_success(request):
    return render(request, 'evaluation/success.html')