from django.contrib import admin
from .models import Etudiant, Travail


@admin.register(Etudiant)
class EtudiantAdmin(admin.ModelAdmin):
    list_display = ('numero_etudiant', 'nom', 'prenom', 'email', 'date_inscription')
    search_fields = ('nom', 'prenom', 'email', 'numero_etudiant')
    list_filter = ('date_inscription',)


@admin.register(Travail)
class TravailAdmin(admin.ModelAdmin):
    list_display = ('titre', 'etudiant', 'date_assignation', 'date_limite', 'statut', 'note')
    search_fields = ('titre', 'etudiant__nom', 'etudiant__prenom', 'etudiant__numero_etudiant')
    list_filter = ('statut', 'date_assignation', 'date_limite')
    date_hierarchy = 'date_assignation'


