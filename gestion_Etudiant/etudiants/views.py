from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q, Avg
from .models import Promotion, Etudiant
from .forms import EtudiantForm


def index(request):
    """Page d'accueil avec liste des promotions"""
    promotions = Promotion.objects.all().order_by('-annee', 'nom')
    context = {
        'promotions': promotions
    }
    return render(request, 'etudiants/index.html', context)


def ajouter_etudiant(request):
    """Vue pour ajouter un nouvel étudiant"""
    if request.method == 'POST':
        form = EtudiantForm(request.POST)
        if form.is_valid():
            etudiant = form.save()
            # Recharger l'étudiant pour avoir le classement mis à jour
            etudiant.refresh_from_db()
            messages.success(
                request, 
                f'Étudiant {etudiant.prenom} {etudiant.nom} ajouté avec succès! '
                f'Classement: {etudiant.classement}ᵉ/{etudiant.promotion.get_nombre_etudiants()}'
            )
            return redirect('classement_promotion', promotion_id=etudiant.promotion.id)
    else:
        form = EtudiantForm()
    
    context = {
        'form': form,
        'promotions': Promotion.objects.all().order_by('-annee', 'nom')
    }
    return render(request, 'etudiants/ajouter_etudiant.html', context)


def classement_promotion(request, promotion_id):
    """Affiche le classement des étudiants d'une promotion"""
    promotion = get_object_or_404(Promotion, id=promotion_id)
    etudiants = Etudiant.objects.filter(promotion=promotion).order_by('classement')
    
    # Calculer les statistiques
    total_etudiants = etudiants.count()
    moyenne_promotion = etudiants.aggregate(
        avg_moyenne=Avg('moyenne_generale')
    )['avg_moyenne'] or 0
    
    meilleure_moyenne = etudiants.first().moyenne_generale if etudiants.exists() else 0
    
    context = {
        'promotion': promotion,
        'etudiants': etudiants,
        'total_etudiants': total_etudiants,
        'moyenne_promotion': moyenne_promotion,
        'meilleure_moyenne': meilleure_moyenne
    }
    return render(request, 'etudiants/classement.html', context)


def api_promotions(request):
    """API pour récupérer les promotions en JSON"""
    promotions = Promotion.objects.all().order_by('-annee', 'nom')
    data = [{
        'id': p.id,
        'nom': p.nom,
        'annee': p.annee,
        'nombre_etudiants': p.get_nombre_etudiants()
    } for p in promotions]
    return JsonResponse(data, safe=False)


def api_classement(request, promotion_id):
    """API pour récupérer le classement d'une promotion en JSON"""
    promotion = get_object_or_404(Promotion, id=promotion_id)
    etudiants = Etudiant.objects.filter(promotion=promotion).order_by('classement')
    data = {
        'promotion': {
            'id': promotion.id,
            'nom': promotion.nom,
            'annee': promotion.annee
        },
        'etudiants': [{
            'id': e.id,
            'nom': e.nom,
            'prenom': e.prenom,
            'numero_etudiant': e.numero_etudiant,
            'moyenne_generale': float(e.moyenne_generale),
            'classement': e.classement
        } for e in etudiants]
    }
    return JsonResponse(data)

