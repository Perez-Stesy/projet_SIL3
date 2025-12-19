from django.db import models
from django.core.validators import MinLengthValidator


class Formateur(models.Model):
    """Modèle pour représenter un formateur"""
    nom = models.CharField(max_length=100, verbose_name="Nom")
    prenom = models.CharField(max_length=100, verbose_name="Prénom")
    email = models.EmailField(unique=True, verbose_name="Email")
    telephone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Téléphone")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    
    class Meta:
        verbose_name = "Formateur"
        verbose_name_plural = "Formateurs"
        ordering = ['nom', 'prenom']
    
    def __str__(self):
        return f"{self.prenom} {self.nom}"


class EspacePedagogique(models.Model):
    """Modèle pour représenter un espace pédagogique"""
    matiere = models.CharField(
        max_length=200, 
        verbose_name="Matière",
        validators=[MinLengthValidator(2)]
    )
    code = models.CharField(
        max_length=50, 
        unique=True, 
        verbose_name="Code",
        validators=[MinLengthValidator(2)]
    )
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    date_creation = models.DateTimeField(auto_now_add=True, verbose_name="Date de création")
    formateurs = models.ManyToManyField(
        Formateur, 
        related_name='espaces_pedagogiques',
        blank=True,
        verbose_name="Formateurs"
    )
    
    class Meta:
        verbose_name = "Espace pédagogique"
        verbose_name_plural = "Espaces pédagogiques"
        ordering = ['matiere']
    
    def __str__(self):
        return f"{self.matiere} ({self.code})"

