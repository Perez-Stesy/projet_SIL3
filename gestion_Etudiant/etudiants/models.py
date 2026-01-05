from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Promotion(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    annee = models.IntegerField()
    description = models.TextField(blank=True)
    date_creation = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-annee', 'nom']

    def __str__(self):
        return f"{self.nom} ({self.annee})"

    def get_nombre_etudiants(self):
        return self.etudiants.count()


class Etudiant(models.Model):
    promotion = models.ForeignKey(Promotion, on_delete=models.CASCADE, related_name='etudiants')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    numero_etudiant = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    date_naissance = models.DateField()
    moyenne_generale = models.FloatField(
        validators=[MinValueValidator(0.0), MaxValueValidator(20.0)],
        default=0.0
    )
    date_inscription = models.DateTimeField(auto_now_add=True)
    classement = models.IntegerField(default=0, editable=False)

    class Meta:
        ordering = ['-moyenne_generale', 'nom', 'prenom']
        unique_together = ['promotion', 'numero_etudiant']

    def __str__(self):
        return f"{self.prenom} {self.nom} - {self.promotion.nom}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_classement()

    def update_classement(self):
        """Met à jour le classement de l'étudiant dans sa promotion"""
        etudiants_promotion = Etudiant.objects.filter(
            promotion=self.promotion
        ).order_by('-moyenne_generale', 'nom', 'prenom')
        
        classement = 1
        for etudiant in etudiants_promotion:
            Etudiant.objects.filter(pk=etudiant.pk).update(classement=classement)
            classement += 1

