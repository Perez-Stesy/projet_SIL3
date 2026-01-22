from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Promotion(models.Model):
    """
    Promotion pour une année donnée.
    Règle: une promotion est unique par année (nom + année).
    """

    name = models.CharField(max_length=120)
    year = models.PositiveIntegerField(
        validators=[MinValueValidator(2000), MaxValueValidator(2100)]
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "year"], name="uniq_promotion_name_year"
            )
        ]
        ordering = ["-year", "name"]

    def __str__(self) -> str:
        return f"{self.name} ({self.year})"


class StudentProfile(models.Model):
    """
    Profil étudiant (User avec role=ETUDIANT) rattaché à une promotion.
    Règle: un étudiant appartient à une seule promotion (par année via la promo).
    """

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="student_profile"
    )
    promotion = models.ForeignKey(
        Promotion, on_delete=models.PROTECT, related_name="students"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["user"], name="uniq_studentprofile_user"),
        ]

    def __str__(self) -> str:
        return f"{self.user.email} -> {self.promotion}"


class Subject(models.Model):
    """
    Matière / module.
    """

    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=200)

    class Meta:
        ordering = ["code"]

    def __str__(self) -> str:
        return f"{self.code} - {self.name}"

from django.db import models

# Create your models here.
