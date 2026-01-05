from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Formateur(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialite = models.CharField(max_length=100)

    def _str_(self):
        return f"{self.user.first_name} {self.user.last_name}"
    
    @property
    def nom(self):
        return self.user.last_name
    
    @property
    def prenom(self):
        return self.user.first_name
    
    @property
    def email(self):
        return self.user.email
    
    
    

