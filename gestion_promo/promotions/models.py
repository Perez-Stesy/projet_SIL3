from django.db import models


class Promotion(models.Model):
    """
    Représente une promotion d'étudiants pour une année donnée.
    Exemple : année 2025, intitulé 'Licence Informatique', code 'L3-INFO-25'.
    """

    year = models.PositiveIntegerField("Année", unique=True)
    name = models.CharField("Intitulé de la promotion", max_length=150)
    code = models.CharField("Code de la promotion", max_length=50, unique=True)
    description = models.TextField("Description", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-year"]

    def __str__(self) -> str:
        return f"{self.year} - {self.name}"