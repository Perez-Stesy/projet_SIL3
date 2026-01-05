from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import Etudiant, Travail
from .serializers import (
    EtudiantSerializer, 
    TravailSerializer, 
    TravailCreateSerializer
)


class EtudiantViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les étudiants"""
    queryset = Etudiant.objects.all()
    serializer_class = EtudiantSerializer


class TravailViewSet(viewsets.ModelViewSet):
    """ViewSet pour gérer les travaux individuels"""
    queryset = Travail.objects.select_related('etudiant').all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return TravailCreateSerializer
        return TravailSerializer

    @action(detail=False, methods=['get'])
    def par_etudiant(self, request):
        """Récupérer tous les travaux d'un étudiant spécifique"""
        etudiant_id = request.query_params.get('etudiant_id')
        if not etudiant_id:
            return Response(
                {'error': 'etudiant_id est requis'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        travaux = self.queryset.filter(etudiant_id=etudiant_id)
        serializer = self.get_serializer(travaux, many=True)
        return Response(serializer.data)
