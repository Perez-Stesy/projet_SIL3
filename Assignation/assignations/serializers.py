from rest_framework import serializers
from .models import Etudiant, Travail


class EtudiantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Etudiant
        fields = ['id', 'nom', 'prenom', 'email', 'numero_etudiant', 'date_creation']


class TravailSerializer(serializers.ModelSerializer):
    etudiant_nom = serializers.SerializerMethodField()
    etudiant_detail = EtudiantSerializer(source='etudiant', read_only=True)
    
    def get_etudiant_nom(self, obj):
        return str(obj.etudiant)

    class Meta:
        model = Travail
        fields = [
            'id', 'titre', 'description', 'date_limite', 
            'date_creation', 'etudiant', 'etudiant_nom', 
            'etudiant_detail', 'statut'
        ]


class TravailCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Travail
        fields = ['titre', 'description', 'date_limite', 'etudiant', 'statut']
