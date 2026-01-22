from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """
    Utilisateur de base avec rôles applicatifs :
    - DIRECTEUR (admin général)
    - FORMATEUR
    - ETUDIANT
    """

    class Roles(models.TextChoices):
        DIRECTEUR = "DIRECTEUR", "Directeur"
        FORMATEUR = "FORMATEUR", "Formateur"
        ETUDIANT = "ETUDIANT", "Étudiant"

    username = models.CharField(max_length=150, blank=True, null=True, unique=False)

    email = models.EmailField(unique=True)
    sexe = models.CharField(
        max_length=10,
        choices=(
            ("HOMME", "Homme"),
            ("FEMME", "Femme"),
            ("AUTRE", "Autre"),
        ),
        blank=True,
    )
    role = models.CharField(
        max_length=20,
        choices=Roles.choices,
        default=Roles.ETUDIANT,
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def is_director(self) -> bool:
        return self.role == self.Roles.DIRECTEUR

    def is_trainer(self) -> bool:
        return self.role == self.Roles.FORMATEUR

    def is_student(self) -> bool:
        return self.role == self.Roles.ETUDIANT

    def save(self, *args, **kwargs):
        # Pour simplifier l’amorçage : tout superuser est considéré comme Directeur.
        if self.is_superuser:
            self.role = self.Roles.DIRECTEUR
        super().save(*args, **kwargs)
