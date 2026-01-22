from rest_framework import generics, mixins, viewsets

from accounts.permissions import IsDirector
from .models import Promotion, StudentProfile, Subject
from .serializers import (
    PromotionSerializer,
    StudentProfileCreateSerializer,
    StudentProfileSerializer,
    SubjectSerializer,
)


class PromotionViewSet(viewsets.ModelViewSet):
    """
    US 2.2: création d'une promotion pour une année donnée.
    Réservé Directeur.
    """

    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsDirector]


class SubjectViewSet(viewsets.ModelViewSet):
    """
    (Support) gestion des matières.
    Réservé Directeur (pour l'instant).
    """

    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = [IsDirector]


class StudentProfileViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    """
    Listing/consultation des étudiants affectés.
    Réservé Directeur.
    """

    queryset = StudentProfile.objects.select_related("user", "promotion").all()
    serializer_class = StudentProfileSerializer
    permission_classes = [IsDirector]


class StudentAssignToPromotionView(generics.CreateAPIView):
    """
    US 2.3: affecter un étudiant (User role=ETUDIANT) à une promotion.
    Réservé Directeur.
    """

    serializer_class = StudentProfileCreateSerializer
    permission_classes = [IsDirector]

from django.shortcuts import render

# Create your views here.
