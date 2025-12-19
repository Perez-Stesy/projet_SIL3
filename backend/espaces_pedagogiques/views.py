from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import EspacePedagogique, Formateur
from .serializers import (
    EspacePedagogiqueSerializer, 
    FormateurSerializer,
    AjouterFormateurSerializer
)


@api_view(['POST'])
def creer_espace_pedagogique(request):
    """
    Créer un nouvel espace pédagogique vide pour une matière
    Epic: Création d'un espace pédagogique vide pour une matière
    """
    serializer = EspacePedagogiqueSerializer(data=request.data)
    
    if serializer.is_valid():
        espace = serializer.save()
        return Response(
            {
                'success': True,
                'message': 'Espace pédagogique créé avec succès',
                'data': EspacePedagogiqueSerializer(espace).data
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {
            'success': False,
            'message': 'Erreur lors de la création de l\'espace pédagogique',
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def lister_espaces_pedagogiques(request):
    """Lister tous les espaces pédagogiques"""
    espaces = EspacePedagogique.objects.all()
    serializer = EspacePedagogiqueSerializer(espaces, many=True)
    return Response(
        {
            'success': True,
            'data': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def detail_espace_pedagogique(request, espace_id):
    """Obtenir les détails d'un espace pédagogique"""
    espace = get_object_or_404(EspacePedagogique, id=espace_id)
    serializer = EspacePedagogiqueSerializer(espace)
    return Response(
        {
            'success': True,
            'data': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def ajouter_formateur_espace(request, espace_id):
    """
    Ajouter un formateur à un espace pédagogique
    Epic: Insertion d'un formateur dans un espace pédagogique
    """
    espace = get_object_or_404(EspacePedagogique, id=espace_id)
    serializer = AjouterFormateurSerializer(data=request.data)
    
    if serializer.is_valid():
        formateur_id = serializer.validated_data['formateur_id']
        formateur = get_object_or_404(Formateur, id=formateur_id)
        
        # Vérifier si le formateur n'est pas déjà dans l'espace
        if espace.formateurs.filter(id=formateur_id).exists():
            return Response(
                {
                    'success': False,
                    'message': 'Ce formateur est déjà assigné à cet espace pédagogique'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Ajouter le formateur
        espace.formateurs.add(formateur)
        
        return Response(
            {
                'success': True,
                'message': 'Formateur ajouté avec succès à l\'espace pédagogique',
                'data': EspacePedagogiqueSerializer(espace).data
            },
            status=status.HTTP_200_OK
        )
    
    return Response(
        {
            'success': False,
            'message': 'Erreur lors de l\'ajout du formateur',
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )


@api_view(['GET'])
def lister_formateurs(request):
    """Lister tous les formateurs disponibles"""
    formateurs = Formateur.objects.all()
    serializer = FormateurSerializer(formateurs, many=True)
    return Response(
        {
            'success': True,
            'data': serializer.data
        },
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def creer_formateur(request):
    """Créer un nouveau formateur"""
    serializer = FormateurSerializer(data=request.data)
    
    if serializer.is_valid():
        formateur = serializer.save()
        return Response(
            {
                'success': True,
                'message': 'Formateur créé avec succès',
                'data': FormateurSerializer(formateur).data
            },
            status=status.HTTP_201_CREATED
        )
    
    return Response(
        {
            'success': False,
            'message': 'Erreur lors de la création du formateur',
            'errors': serializer.errors
        },
        status=status.HTTP_400_BAD_REQUEST
    )

