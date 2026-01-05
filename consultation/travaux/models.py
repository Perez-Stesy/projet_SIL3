from django.db import models


class Etudiant(models.Model):
    """Modèle pour représenter un étudiant"""
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    numero_etudiant = models.CharField(max_length=20, unique=True)
    date_inscription = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.prenom} {self.nom} ({self.numero_etudiant})"


class Travail(models.Model):
    """Modèle pour représenter un travail assigné à un étudiant"""
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('en_cours', 'En cours'),
        ('termine', 'Terminé'),
        ('en_retard', 'En retard'),
    ]

    titre = models.CharField(max_length=200)
    description = models.TextField()
    etudiant = models.ForeignKey(Etudiant, on_delete=models.CASCADE, related_name='travaux')
    date_assignation = models.DateField(auto_now_add=True)
    date_limite = models.DateField()
    statut = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    note = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    commentaire = models.TextField(blank=True)

    class Meta:
        verbose_name = "Travail"
        verbose_name_plural = "Travaux"
        ordering = ['-date_assignation']

    def __str__(self):
        return f"{self.titre} - {self.etudiant}"


