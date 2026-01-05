from django.db import models

from django.contrib.auth.models import User

# Create your models here.

class Travail(models.Model):
    TYPE_CHOICES = [
        ('individuel',
         'Individuel'),
        ('collectif',
          'Collectif'),
    ]
    titre = models.CharField(max_length=100)
    consigne = models.TextField()
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    formateur = models.ForeignKey(User, on_delete=models.CASCADE, related_name='travaux_formateur')
    date_creation = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.titre
