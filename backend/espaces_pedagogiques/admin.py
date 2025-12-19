from django.contrib import admin
from .models import EspacePedagogique, Formateur


@admin.register(Formateur)
class FormateurAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'email', 'telephone', 'date_creation')
    search_fields = ('nom', 'prenom', 'email')
    list_filter = ('date_creation',)


@admin.register(EspacePedagogique)
class EspacePedagogiqueAdmin(admin.ModelAdmin):
    list_display = ('matiere', 'code', 'date_creation', 'nombre_formateurs')
    search_fields = ('matiere', 'code')
    list_filter = ('date_creation',)
    filter_horizontal = ('formateurs',)
    
    def nombre_formateurs(self, obj):
        return obj.formateurs.count()
    nombre_formateurs.short_description = "Nombre de formateurs"

