from rest_framework import serializers
from .models import EspacePedagogique, Formateur


class FormateurSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle Formateur"""
    class Meta:
        model = Formateur
        fields = ['id', 'nom', 'prenom', 'email', 'telephone', 'date_creation']


class EspacePedagogiqueSerializer(serializers.ModelSerializer):
    """Serializer pour le modèle EspacePedagogique"""
    formateurs = FormateurSerializer(many=True, read_only=True)
    nombre_formateurs = serializers.SerializerMethodField()
    
    class Meta:
        model = EspacePedagogique
        fields = ['id', 'matiere', 'code', 'description', 'date_creation', 'formateurs', 'nombre_formateurs']
        read_only_fields = ['id', 'date_creation']
    
    def get_nombre_formateurs(self, obj):
        return obj.formateurs.count()
    
    def validate_code(self, value):
        """Valider que le code est unique"""
        if self.instance and self.instance.code == value:
            return value
        if EspacePedagogique.objects.filter(code=value).exists():
            raise serializers.ValidationError("Un espace pédagogique avec ce code existe déjà.")
        return value


class AjouterFormateurSerializer(serializers.Serializer):
    """Serializer pour ajouter un formateur à un espace pédagogique"""
    formateur_id = serializers.IntegerField(required=True)
    
    def validate_formateur_id(self, value):
        if not Formateur.objects.filter(id=value).exists():
            raise serializers.ValidationError("Ce formateur n'existe pas.")
        return value

