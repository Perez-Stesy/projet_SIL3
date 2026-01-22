from django.db.models import Avg
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsDirector, IsStudent, IsTrainer
from academics.models import Promotion, StudentProfile
from .models import Evaluation, Submission, Work, WorkAssignment
from .serializers import (
    EvaluationCreateSerializer,
    EvaluationSerializer,
    StudentMyAssignmentsSerializer,
    SubmissionCreateSerializer,
    SubmissionSerializer,
    WorkAssignmentSerializer,
    WorkSerializer,
)


class WorkViewSet(viewsets.ModelViewSet):
    """
    US 5.1: création d'un travail par formateur affecté à l'espace.
    Réservé Formateur (affectation vérifiée dans le serializer).
    """

    queryset = Work.objects.select_related("space", "created_by", "space__subject").all()
    serializer_class = WorkSerializer
    permission_classes = [IsTrainer]

    def get_queryset(self):
        # Un formateur ne voit que les travaux des espaces où il est affecté.
        user = self.request.user
        return super().get_queryset().filter(space__trainers__id=user.id).distinct()


class WorkAssignmentViewSet(viewsets.ModelViewSet):
    """
    US 6.1: assignation d'un travail individuel à un étudiant.
    Réservé Formateur.
    """

    queryset = WorkAssignment.objects.select_related(
        "work", "student", "student__user", "work__space"
    ).all()
    serializer_class = WorkAssignmentSerializer
    permission_classes = [IsTrainer]

    def get_queryset(self):
        # Un formateur ne voit que les assignations liées à ses espaces.
        user = self.request.user
        return super().get_queryset().filter(work__space__trainers__id=user.id).distinct()

    def perform_create(self, serializer):
        # Validation d'appartenance à l'espace faite dans serializer.
        serializer.save()


class StudentMyAssignmentsView(generics.ListAPIView):
    """
    US 7.1: consultation des travaux assignés par l'étudiant (uniquement les siens).
    """

    serializer_class = StudentMyAssignmentsSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        user = self.request.user
        try:
            profile = StudentProfile.objects.get(user_id=user.id)
        except StudentProfile.DoesNotExist:
            return WorkAssignment.objects.none()
        return (
            WorkAssignment.objects.select_related("work", "work__space")
            .filter(student=profile)
            .order_by("-assigned_at")
        )


class SubmissionCreateView(generics.CreateAPIView):
    """
    US 8.1: livraison d'un travail individuel (par assignment).
    """

    serializer_class = SubmissionCreateSerializer
    permission_classes = [IsStudent]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()
        out = SubmissionSerializer(submission, context={"request": request})
        return Response(out.data, status=status.HTTP_201_CREATED)


class StudentMySubmissionsView(generics.ListAPIView):
    """
    (Support) liste des livraisons de l'étudiant authentifié.
    """

    serializer_class = SubmissionSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        user = self.request.user
        return Submission.objects.select_related(
            "assignment", "assignment__student", "assignment__student__user"
        ).filter(assignment__student__user_id=user.id)


class TrainerMySubmissionsView(generics.ListAPIView):
    """
    Liste des livraisons à évaluer pour le formateur (espaces où il est affecté).
    """

    serializer_class = SubmissionSerializer
    permission_classes = [IsTrainer]

    def get_queryset(self):
        user = self.request.user
        return Submission.objects.select_related(
            "assignment",
            "assignment__work",
            "assignment__work__space",
            "assignment__student",
            "assignment__student__user",
        ).filter(assignment__work__space__trainers__id=user.id)


class EvaluationCreateView(generics.CreateAPIView):
    """
    US 9.1: évaluer un travail livré.
    """

    serializer_class = EvaluationCreateSerializer
    permission_classes = [IsTrainer]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        evaluation = serializer.save()
        out = EvaluationSerializer(evaluation, context={"request": request})
        return Response(out.data, status=status.HTTP_201_CREATED)


class StudentMyEvaluationsView(generics.ListAPIView):
    """
    US 10.1: consultation des évaluations (uniquement les siennes, publiées).
    """

    serializer_class = EvaluationSerializer
    permission_classes = [IsStudent]

    def get_queryset(self):
        user = self.request.user
        return Evaluation.objects.select_related(
            "submission",
            "submission__assignment",
            "submission__assignment__student",
            "submission__assignment__student__user",
            "submission__assignment__work",
        ).filter(
            submission__assignment__student__user_id=user.id,
            published=True,
        )


class PromotionRankingView(generics.GenericAPIView):
    """
    US 11.1: classement général d'une promotion pour une année donnée (moyennes).
    Accessible Directeur, Formateur, Étudiant.
    """

    permission_classes = [IsDirector | IsTrainer | IsStudent]

    def get(self, request, *args, **kwargs):
        promotion_id = request.query_params.get("promotion_id")
        year = request.query_params.get("year")
        if not promotion_id or not year:
            return Response(
                {"detail": "promotion_id et year sont requis."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            promotion = Promotion.objects.get(id=promotion_id, year=int(year))
        except (Promotion.DoesNotExist, ValueError):
            return Response(
                {"detail": "Promotion inexistante."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Moyenne par étudiant sur les évaluations publiées de l'année/promotion.
        qs = (
            Evaluation.objects.filter(
                published=True,
                submission__assignment__student__promotion=promotion,
                submission__assignment__work__space__year=promotion.year,
            )
            .values("submission__assignment__student_id", "submission__assignment__student__user__email")
            .annotate(avg_grade=Avg("grade"))
            .order_by("-avg_grade")
        )

        if not qs.exists():
            return Response(
                {"detail": "Aucune évaluation."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        results = []
        rank = 1
        for row in qs:
            results.append(
                {
                    "rank": rank,
                    "student_profile_id": row["submission__assignment__student_id"],
                    "email": row["submission__assignment__student__user__email"],
                    "average": row["avg_grade"],
                }
            )
            rank += 1

        return Response(
            {
                "promotion": {"id": promotion.id, "name": promotion.name, "year": promotion.year},
                "results": results,
            }
        )

from django.shortcuts import render

# Create your views here.
