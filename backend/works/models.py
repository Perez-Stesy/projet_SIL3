from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from academics.models import StudentProfile
from pedagogy.models import PedagogicalSpace


class Work(models.Model):
    """
    US 5.1: création d'un travail (individuel/collectif) par un Formateur affecté.
    """

    class Types(models.TextChoices):
        INDIVIDUAL = "INDIVIDUAL", "Individuel"
        COLLECTIVE = "COLLECTIVE", "Collectif"

    space = models.ForeignKey(PedagogicalSpace, on_delete=models.CASCADE, related_name="works")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_works"
    )
    type = models.CharField(max_length=20, choices=Types.choices)
    title = models.CharField(max_length=200)
    instructions = models.TextField()
    due_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self) -> str:
        return f"{self.title} ({self.type})"


class WorkAssignment(models.Model):
    """
    US 6.1: assignation d'un travail individuel à un étudiant.
    """

    work = models.ForeignKey(Work, on_delete=models.CASCADE, related_name="assignments")
    student = models.ForeignKey(
        StudentProfile, on_delete=models.CASCADE, related_name="assignments"
    )
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["work", "student"], name="uniq_work_student")
        ]
        ordering = ["-assigned_at"]

    def __str__(self) -> str:
        return f"{self.work_id} -> {self.student_id}"


def submission_upload_to(instance, filename: str) -> str:
    return f"submissions/work_{instance.assignment.work_id}/student_{instance.assignment.student_id}/{filename}"


class Submission(models.Model):
    """
    US 8.1: livraison d'un travail individuel.
    Règle: une seule livraison par assignation (par défaut).
    """

    assignment = models.OneToOneField(
        WorkAssignment, on_delete=models.CASCADE, related_name="submission"
    )
    file = models.FileField(upload_to=submission_upload_to)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"Submission {self.id} (assignment={self.assignment_id})"


class Evaluation(models.Model):
    """
    US 9.1: évaluation d'un travail livré par un Formateur.
    """

    submission = models.OneToOneField(
        Submission, on_delete=models.CASCADE, related_name="evaluation"
    )
    evaluator = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="evaluations"
    )
    grade = models.DecimalField(max_digits=5, decimal_places=2, validators=[MinValueValidator(0)])
    max_grade = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(1)],
        default=20,
    )
    comment = models.TextField(blank=True)
    published = models.BooleanField(default=False)
    evaluated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-evaluated_at"]

    def __str__(self) -> str:
        return f"Eval submission={self.submission_id} {self.grade}/{self.max_grade}"

from django.db import models

# Create your models here.
