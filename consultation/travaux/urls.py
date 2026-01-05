from django.urls import path
from . import views

urlpatterns = [
    path('etudiants/', views.get_etudiants, name='get_etudiants'),
    path('etudiants/<int:etudiant_id>/travaux/', views.get_travaux_par_etudiant, name='get_travaux_par_etudiant'),
    path('etudiants/<str:numero_etudiant>/travaux/', views.get_travaux_par_numero, name='get_travaux_par_numero'),
]


