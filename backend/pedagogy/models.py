from django.conf import settings
from django.db import models

from academics.models import Promotion, StudentProfile, Subject


class PedagogicalSpace(models.Model):
    """
    US 3.1: espace pédagogique vide pour une matière, pour une année.
    Règle: unique par (matière, année).
    """

    subject = models.ForeignKey(Subject, on_delete=models.PROTECT, related_name="spaces")
    year = models.PositiveIntegerField()
    promotion = models.ForeignKey(
        Promotion, on_delete=models.PROTECT, related_name="spaces"
    )
    trainers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, blank=True, related_name="trainer_spaces"
    )
    students = models.ManyToManyField(StudentProfile, blank=True, related_name="spaces")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["subject", "year"], name="uniq_space_subject_year"
            )
        ]
        ordering = ["-year", "subject__code"]

    def __str__(self) -> str:
        return f"{self.subject} - {self.year}"

from django.db import models

# Create your models here.
