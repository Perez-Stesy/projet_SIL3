from django.contrib import admin

from .models import Promotion

admin.site.register(Promotion)

from django.core.exceptions import ValidationError
from django import forms
from django.utils import timezone
from .models import Promotion


class PromotionAdminForm(forms.ModelForm):
    """Formulaire personnalisé pour l'admin avec validation"""
    
    class Meta:
        model = Promotion
        fields = '__all__'
    
    def clean(self):
        cleaned_data = super().clean()
        nom = cleaned_data.get('nom')
        annee = cleaned_data.get('annee')
        
        if nom and annee:
            # Vérifier que l'année n'est pas antérieure à l'année en cours
            annee_actuelle = timezone.now().year
            if annee < annee_actuelle:
                raise ValidationError({
                    'annee': f"Impossible de créer une promotion pour l'année {annee}. "
                             f"L'année doit être supérieure ou égale à {annee_actuelle}."
                })
            
            # Vérifier qu'il n'existe pas déjà une promotion avec le même nom et la même année
            if self.instance.pk:  # Modification
                existing = Promotion.objects.filter(nom=nom, annee=annee).exclude(pk=self.instance.pk)
            else:  # Création
                existing = Promotion.objects.filter(nom=nom, annee=annee)
            
            if existing.exists():
                raise ValidationError({
                    'nom': f"Une promotion avec le nom '{nom}' et l'année {annee} existe déjà.",
                    'annee': f"Une promotion avec le nom '{nom}' et l'année {annee} existe déjà."
                })
        
        return cleaned_data


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    form = PromotionAdminForm
    list_display = ('nom', 'annee', 'date_debut', 'date_fin', 'nombre_etudiants', 'active', 'est_en_cours')
    list_filter = ('annee', 'active', 'date_debut', 'date_fin')
    search_fields = ('nom', 'description', 'annee')
    date_hierarchy = 'date_debut'
    readonly_fields = ('date_creation', 'date_modification', 'duree_jours', 'est_en_cours')
    fieldsets = (
        ('Informations générales', {
            'fields': ('nom', 'annee', 'description', 'couleur')
        }),
        ('Dates', {
            'fields': ('date_debut', 'date_fin', 'duree_jours')
        }),
        ('Statistiques', {
            'fields': ('nombre_etudiants', 'active', 'est_en_cours')
        }),
        ('Métadonnées', {
            'fields': ('date_creation', 'date_modification'),
            'classes': ('collapse',)
        }),
    )

