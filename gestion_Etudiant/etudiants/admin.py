from django.contrib import admin
from .models import Promotion, Etudiant


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['nom', 'annee', 'get_nombre_etudiants', 'date_creation']
    list_filter = ['annee']
    search_fields = ['nom', 'description']


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ['nom', 'prenom', 'numero_etudiant', 'promotion', 'moyenne_generale', 'classement']
    list_filter = ['promotion', 'date_inscription']
    search_fields = ['nom', 'prenom', 'numero_etudiant', 'email']
    ordering = ['promotion', 'classement']

