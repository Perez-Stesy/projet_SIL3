from django.db import models


class Etudiant(models.Model):
    """Modèle représentant un étudiant"""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    numero_etudiant = models.CharField(max_length=20, unique=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['nom', 'prenom']
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.numero_etudiant})"


class Travail(models.Model):
    """Modèle représentant un travail individuel"""
    titre = models.CharField(max_length=200)
    description = models.TextField()
    date_limite = models.DateTimeField()
    date_creation = models.DateTimeField(auto_now_add=True)
    etudiant = models.ForeignKey(
        Etudiant,
        on_delete=models.CASCADE,
        related_name='travaux',
        verbose_name="Étudiant assigné"
    )
    statut = models.CharField(
        max_length=20,
        choices=[
            ('en_attente', 'En attente'),
            ('en_cours', 'En cours'),
            ('termine', 'Terminé'),
        ],
        default='en_attente'
    )

    class Meta:
        ordering = ['-date_creation']
        verbose_name = "Travail"
        verbose_name_plural = "Travaux"

    def __str__(self):
        return f"{self.titre} - {self.etudiant}"
