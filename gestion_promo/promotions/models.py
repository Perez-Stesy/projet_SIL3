from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


class Promotion(models.Model):
    """Modèle pour représenter une promotion pour une année donnée"""
    
    nom = models.CharField(
        max_length=200,
        verbose_name="Nom de la promotion",
        help_text="Ex: Promotion 2024-2025, Master Informatique 2024, etc."
    )
    annee = models.IntegerField(
        validators=[
            MinValueValidator(2000),
            MaxValueValidator(2100)
        ],
        verbose_name="Année",
        help_text="Année de la promotion"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Description",
        help_text="Description détaillée de la promotion"
    )
    date_debut = models.DateField(
        verbose_name="Date de début",
        help_text="Date de début de la promotion"
    )
    date_fin = models.DateField(
        verbose_name="Date de fin",
        help_text="Date de fin de la promotion"
    )
    nombre_etudiants = models.PositiveIntegerField(
        default=0,
        verbose_name="Nombre d'étudiants",
        help_text="Nombre d'étudiants dans cette promotion"
    )
    active = models.BooleanField(
        default=True,
        verbose_name="Active",
        help_text="Indique si la promotion est actuellement active"
    )
    couleur = models.CharField(
        max_length=7,
        default="#6366f1",
        verbose_name="Couleur",
        help_text="Couleur associée à la promotion (format hexadécimal)"
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date de création"
    )
    date_modification = models.DateTimeField(
        auto_now=True,
        verbose_name="Date de modification"
    )
    
    class Meta:
        verbose_name = "Promotion"
        verbose_name_plural = "Promotions"
        ordering = ['-annee', '-date_creation']
        unique_together = ['nom', 'annee']
    
    def clean(self):
        """Valide les contraintes métier"""
        annee_actuelle = timezone.now().year
        if self.annee < annee_actuelle:
            raise ValidationError({
                'annee': f"Impossible de créer une promotion pour l'année {self.annee}. L'année doit être supérieure ou égale à {annee_actuelle}."
            })
        if self.pk:
            existing = Promotion.objects.filter(nom=self.nom, annee=self.annee).exclude(pk=self.pk)
        else:
            existing = Promotion.objects.filter(nom=self.nom, annee=self.annee)
        if existing.exists():
            raise ValidationError({
                'nom': f"Une promotion avec le nom '{self.nom}' et l'année {self.annee} existe déjà.",
                'annee': f"Une promotion avec le nom '{self.nom}' et l'année {self.annee} existe déjà."
            })
    
    def save(self, *args, **kwargs):
        """Surcharge de save pour appeler clean()"""
        self.full_clean()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} - {self.annee}"
    
    @property
    def duree_jours(self):
        """Calcule la durée de la promotion en jours"""
        return (self.date_fin - self.date_debut).days
    
    @property
    def est_en_cours(self):
        """Vérifie si la promotion est actuellement en cours"""
        aujourdhui = timezone.now().date()
        return self.active and self.date_debut <= aujourdhui <= self.date_fin
