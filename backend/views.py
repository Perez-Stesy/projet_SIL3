from django.http import JsonResponse
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def api_root(request):
    """Page d'accueil de l'API"""
    return JsonResponse({
        'message': 'Bienvenue sur l\'API de gestion des espaces pédagogiques',
        'version': '1.0',
        'endpoints': {
            'espaces_pedagogiques': {
                'liste': '/api/espaces/',
                'creer': '/api/espaces/creer/',
                'detail': '/api/espaces/<id>/',
                'ajouter_formateur': '/api/espaces/<id>/ajouter-formateur/',
            },
            'formateurs': {
                'liste': '/api/formateurs/',
                'creer': '/api/formateurs/creer/',
            },
            'admin': '/admin/',
        },
        'documentation': 'Voir API_DOCUMENTATION.md pour plus de détails',
        'frontend': 'Ouvrez frontend/index.html dans votre navigateur'
    })

