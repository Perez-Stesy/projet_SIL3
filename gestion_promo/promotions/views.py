from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
from .models import Promotion
from datetime import datetime


def index(request):
    """Vue principale qui sert la page HTML"""
    return render(request, 'promotions/index.html')


@csrf_exempt
@require_http_methods(["GET"])
def api_list_promotions(request):
    """API pour lister toutes les promotions"""
    promotions = Promotion.objects.all()
    data = []
    for promo in promotions:
        data.append({
            'id': promo.id,
            'nom': promo.nom,
            'annee': promo.annee,
            'description': promo.description or '',
            'date_debut': promo.date_debut.isoformat(),
            'date_fin': promo.date_fin.isoformat(),
            'nombre_etudiants': promo.nombre_etudiants,
            'active': promo.active,
            'couleur': promo.couleur,
            'duree_jours': promo.duree_jours,
            'est_en_cours': promo.est_en_cours,
            'date_creation': promo.date_creation.isoformat(),
        })
    return JsonResponse({'promotions': data}, safe=False)


@csrf_exempt
@require_http_methods(["POST"])
def api_create_promotion(request):
    """API pour créer une nouvelle promotion"""
    try:
        data = json.loads(request.body)
        
        # Validation des champs requis
        nom = data.get('nom', '').strip()
        annee = data.get('annee')
        date_debut = data.get('date_debut')
        date_fin = data.get('date_fin')
        
        if not nom:
            return JsonResponse({'error': 'Le nom est requis'}, status=400)
        
        if not annee:
            return JsonResponse({'error': "L'année est requise"}, status=400)
        
        if not date_debut:
            return JsonResponse({'error': 'La date de début est requise'}, status=400)
        
        if not date_fin:
            return JsonResponse({'error': 'La date de fin est requise'}, status=400)
        
        # Conversion des dates
        try:
            date_debut = datetime.fromisoformat(date_debut.replace('Z', '+00:00')).date()
            date_fin = datetime.fromisoformat(date_fin.replace('Z', '+00:00')).date()
        except ValueError:
            return JsonResponse({'error': 'Format de date invalide'}, status=400)
        
        # Vérification que la date de fin est après la date de début
        if date_fin < date_debut:
            return JsonResponse({'error': 'La date de fin doit être après la date de début'}, status=400)
        
        # Création de la promotion
        promotion = Promotion.objects.create(
            nom=nom,
            annee=annee,
            description=data.get('description', '').strip(),
            date_debut=date_debut,
            date_fin=date_fin,
            nombre_etudiants=data.get('nombre_etudiants', 0),
            active=data.get('active', True),
            couleur=data.get('couleur', '#6366f1'),
        )
        
        return JsonResponse({
            'success': True,
            'promotion': {
                'id': promotion.id,
                'nom': promotion.nom,
                'annee': promotion.annee,
                'description': promotion.description or '',
                'date_debut': promotion.date_debut.isoformat(),
                'date_fin': promotion.date_fin.isoformat(),
                'nombre_etudiants': promotion.nombre_etudiants,
                'active': promotion.active,
                'couleur': promotion.couleur,
                'duree_jours': promotion.duree_jours,
                'est_en_cours': promotion.est_en_cours,
            }
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["GET"])
def api_get_promotion(request, promotion_id):
    """API pour récupérer une promotion spécifique"""
    try:
        promotion = Promotion.objects.get(id=promotion_id)
        return JsonResponse({
            'id': promotion.id,
            'nom': promotion.nom,
            'annee': promotion.annee,
            'description': promotion.description or '',
            'date_debut': promotion.date_debut.isoformat(),
            'date_fin': promotion.date_fin.isoformat(),
            'nombre_etudiants': promotion.nombre_etudiants,
            'active': promotion.active,
            'couleur': promotion.couleur,
            'duree_jours': promotion.duree_jours,
            'est_en_cours': promotion.est_en_cours,
        })
    except Promotion.DoesNotExist:
        return JsonResponse({'error': 'Promotion non trouvée'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["PUT"])
def api_update_promotion(request, promotion_id):
    """API pour modifier une promotion"""
    try:
        promotion = Promotion.objects.get(id=promotion_id)
        data = json.loads(request.body)
        
        # Mise à jour des champs
        if 'nom' in data:
            promotion.nom = data['nom'].strip()
        if 'annee' in data:
            promotion.annee = data['annee']
        if 'description' in data:
            promotion.description = data['description'].strip()
        if 'date_debut' in data:
            try:
                promotion.date_debut = datetime.fromisoformat(data['date_debut'].replace('Z', '+00:00')).date()
            except ValueError:
                return JsonResponse({'error': 'Format de date de début invalide'}, status=400)
        if 'date_fin' in data:
            try:
                promotion.date_fin = datetime.fromisoformat(data['date_fin'].replace('Z', '+00:00')).date()
            except ValueError:
                return JsonResponse({'error': 'Format de date de fin invalide'}, status=400)
        if 'nombre_etudiants' in data:
            promotion.nombre_etudiants = int(data['nombre_etudiants'])
        if 'active' in data:
            promotion.active = data['active']
        if 'couleur' in data:
            promotion.couleur = data['couleur']
        
        # Validation
        if promotion.date_fin < promotion.date_debut:
            return JsonResponse({'error': 'La date de fin doit être après la date de début'}, status=400)
        
        promotion.save()
        
        return JsonResponse({
            'success': True,
            'promotion': {
                'id': promotion.id,
                'nom': promotion.nom,
                'annee': promotion.annee,
                'description': promotion.description or '',
                'date_debut': promotion.date_debut.isoformat(),
                'date_fin': promotion.date_fin.isoformat(),
                'nombre_etudiants': promotion.nombre_etudiants,
                'active': promotion.active,
                'couleur': promotion.couleur,
                'duree_jours': promotion.duree_jours,
                'est_en_cours': promotion.est_en_cours,
            }
        })
        
    except Promotion.DoesNotExist:
        return JsonResponse({'error': 'Promotion non trouvée'}, status=404)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Données JSON invalides'}, status=400)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def api_delete_promotion(request, promotion_id):
    """API pour supprimer une promotion"""
    try:
        promotion = Promotion.objects.get(id=promotion_id)
        promotion.delete()
        return JsonResponse({'success': True, 'message': 'Promotion supprimée avec succès'})
    except Promotion.DoesNotExist:
        return JsonResponse({'error': 'Promotion non trouvée'}, status=404)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
