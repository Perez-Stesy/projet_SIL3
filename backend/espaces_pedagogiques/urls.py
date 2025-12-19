from django.urls import path
from . import views

app_name = 'espaces_pedagogiques'

urlpatterns = [
    # Epic 1: Création d'un espace pédagogique vide
    path('espaces/', views.lister_espaces_pedagogiques, name='lister_espaces'),
    path('espaces/creer/', views.creer_espace_pedagogique, name='creer_espace'),
    path('espaces/<int:espace_id>/', views.detail_espace_pedagogique, name='detail_espace'),
    
    # Epic 2: Insertion d'un formateur dans un espace pédagogique
    path('espaces/<int:espace_id>/ajouter-formateur/', views.ajouter_formateur_espace, name='ajouter_formateur'),
    
    # Gestion des formateurs
    path('formateurs/', views.lister_formateurs, name='lister_formateurs'),
    path('formateurs/creer/', views.creer_formateur, name='creer_formateur'),
]

