from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from accounts.permissions import IsDirector, IsStudent, IsTrainer
from academics.models import StudentProfile
from .models import PedagogicalSpace
from .serializers import (
    AddStudentToSpaceSerializer,
    AssignTrainerSerializer,
    PedagogicalSpaceSerializer,
    SpaceDetailSerializer,
)


class PedagogicalSpaceViewSet(viewsets.ModelViewSet):
    """
    US 3.1: créer un espace pédagogique (vide).
    US 3.5: consulter tous les espaces.
    Réservé Directeur.
    """

    queryset = PedagogicalSpace.objects.select_related(
        "subject", "promotion"
    ).prefetch_related("trainers", "students", "students__user")
    serializer_class = PedagogicalSpaceSerializer
    permission_classes = [IsDirector]

    def get_serializer_class(self):
        if self.action in {"list", "retrieve"}:
            return SpaceDetailSerializer
        return super().get_serializer_class()

    @action(detail=True, methods=["post"], url_path="assign-trainer")
    def assign_trainer(self, request, pk=None):
        """
        US 3.2: affectation formateur.
        """
        space = self.get_object()
        serializer = AssignTrainerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        trainer_id = serializer.validated_data["trainer_user_id"]

        if space.trainers.filter(id=trainer_id).exists():
            return Response(
                {"detail": "Formateur déjà affecté."}, status=status.HTTP_400_BAD_REQUEST
            )

        space.trainers.add(trainer_id)
        return Response({"detail": "Formateur affecté avec succès."})

    @action(detail=True, methods=["post"], url_path="add-student")
    def add_student(self, request, pk=None):
        """
        US 3.3: ajout étudiant (doit appartenir à la promotion concernée).
        """
        space = self.get_object()
        serializer = AddStudentToSpaceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        student_profile_id = serializer.validated_data["student_profile_id"]

        try:
            student_profile = StudentProfile.objects.select_related(
                "promotion", "user"
            ).get(id=student_profile_id)
        except StudentProfile.DoesNotExist:
            return Response(
                {"detail": "Étudiant inexistant."}, status=status.HTTP_400_BAD_REQUEST
            )

        if student_profile.promotion_id != space.promotion_id:
            return Response(
                {"detail": "Étudiant hors promotion (action refusée)."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if space.students.filter(id=student_profile_id).exists():
            return Response(
                {"detail": "Étudiant déjà inscrit."}, status=status.HTTP_400_BAD_REQUEST
            )

        space.students.add(student_profile)
        return Response({"detail": "Étudiant ajouté avec succès."})

    @action(detail=False, methods=["get"], url_path="me/formateur", permission_classes=[IsTrainer])
    def mes_espaces_formateur(self, request):
        """
        Liste des espaces où le formateur connecté est affecté.
        """
        qs = self.get_queryset().filter(trainers__id=request.user.id).distinct()
        serializer = SpaceDetailSerializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=["get"], url_path="me/etudiant", permission_classes=[IsStudent])
    def mes_espaces_etudiant(self, request):
        """
        Liste des espaces où l'étudiant connecté est inscrit.
        """
        try:
            profile = StudentProfile.objects.get(user_id=request.user.id)
        except StudentProfile.DoesNotExist:
            return Response([])
        qs = self.get_queryset().filter(students__id=profile.id).distinct()
        serializer = SpaceDetailSerializer(qs, many=True)
        return Response(serializer.data)

