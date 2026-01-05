from django.contrib import admin
from .models import Etudiant, Travail


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('numero_etudiant', 'nom', 'prenom', 'email', 'date_creation')
    search_fields = ('nom', 'prenom', 'email', 'numero_etudiant')
    list_filter = ('date_creation',)


@admin.register(Travail)
class TravailAdmin(admin.ModelAdmin):
    list_display = ('titre', 'etudiant', 'statut', 'date_limite', 'date_creation')
    search_fields = ('titre', 'description', 'etudiant__nom', 'etudiant__prenom')
    list_filter = ('statut', 'date_limite', 'date_creation')
    date_hierarchy = 'date_limite'
