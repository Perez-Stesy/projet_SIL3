from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Travail(models.Model):
    titre=models.CharField(max_length=100)
    contenu=models.TextField()
    apprenant=models.ForeignKey(User, on_delete=models.CASCADE, related_name='travaux_apprenant')
    date_livraison=models.DateTimeField(auto_now_add=True)

    def str(self):
        return self.titre
    
class Evaluation(models.Model):
    travail=models.OneToOneField(Travail, on_delete=models.CASCADE)
    formateur = models.ForeignKey(User, on_delete=models.CASCADE)
    note=models.FloatField()
    commentaire= models.TextField()
    date_evaluation= models.DateTimeField(auto_now_add=True)

    def str(self):
        return f"Evaluation de {self.travail.titre}"
