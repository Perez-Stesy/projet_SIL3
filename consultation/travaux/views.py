from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
import json
from .models import Etudiant, Travail


@csrf_exempt
@require_http_methods(["GET"])
def get_etudiants(request):
    """Récupère la liste de tous les étudiants"""
    etudiants = Etudiant.objects.all()
    data = [
        {
            'id': etudiant.id,
            'nom': etudiant.nom,
            'prenom': etudiant.prenom,
            'email': etudiant.email,
            'numero_etudiant': etudiant.numero_etudiant,
        }
        for etudiant in etudiants
    ]
    return JsonResponse({'etudiants': data}, safe=False)


@csrf_exempt
@require_http_methods(["GET"])
def get_travaux_par_etudiant(request, etudiant_id):
    """Récupère tous les travaux assignés à un étudiant donné"""
    try:
        etudiant = Etudiant.objects.get(id=etudiant_id)
        travaux = Travail.objects.filter(etudiant=etudiant)
        
        data = {
            'etudiant': {
                'id': etudiant.id,
                'nom': etudiant.nom,
                'prenom': etudiant.prenom,
                'email': etudiant.email,
                'numero_etudiant': etudiant.numero_etudiant,
            },
            'travaux': [
                {
                    'id': travail.id,
                    'titre': travail.titre,
                    'description': travail.description,
                    'date_assignation': travail.date_assignation.strftime('%Y-%m-%d'),
                    'date_limite': travail.date_limite.strftime('%Y-%m-%d'),
                    'statut': travail.statut,
                    'statut_display': travail.get_statut_display(),
                    'note': float(travail.note) if travail.note else None,
                    'commentaire': travail.commentaire,
                }
                for travail in travaux
            ]
        }
        return JsonResponse(data, safe=False)
    except Etudiant.DoesNotExist:
        return JsonResponse({'error': 'Étudiant non trouvé'}, status=404)


@csrf_exempt
@require_http_methods(["GET"])
def get_travaux_par_numero(request, numero_etudiant):
    """Récupère tous les travaux assignés à un étudiant par son numéro"""
    try:
        etudiant = Etudiant.objects.get(numero_etudiant=numero_etudiant)
        travaux = Travail.objects.filter(etudiant=etudiant)
        
        data = {
            'etudiant': {
                'id': etudiant.id,
                'nom': etudiant.nom,
                'prenom': etudiant.prenom,
                'email': etudiant.email,
                'numero_etudiant': etudiant.numero_etudiant,
            },
            'travaux': [
                {
                    'id': travail.id,
                    'titre': travail.titre,
                    'description': travail.description,
                    'date_assignation': travail.date_assignation.strftime('%Y-%m-%d'),
                    'date_limite': travail.date_limite.strftime('%Y-%m-%d'),
                    'statut': travail.statut,
                    'statut_display': travail.get_statut_display(),
                    'note': float(travail.note) if travail.note else None,
                    'commentaire': travail.commentaire,
                }
                for travail in travaux
            ]
        }
        return JsonResponse(data, safe=False)
    except Etudiant.DoesNotExist:
        return JsonResponse({'error': 'Étudiant non trouvé'}, status=404)


