from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import User
from .models import Promotion, StudentProfile, Subject

UserModel = get_user_model()


class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = ["id", "name", "year", "created_at"]


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ["id", "code", "name"]


class StudentProfileCreateSerializer(serializers.Serializer):
    """
    US 2.3: création d'un étudiant pour une promotion donnée.
    On s'appuie sur un User existant (créé en US 1.1) avec role=ETUDIANT.
    """

    student_user_id = serializers.IntegerField()
    promotion_id = serializers.IntegerField()

    def validate(self, attrs):
        try:
            user = UserModel.objects.get(id=attrs["student_user_id"])
        except UserModel.DoesNotExist:
            raise serializers.ValidationError({"student_user_id": "Étudiant inexistant."})

        if getattr(user, "role", None) != User.Roles.ETUDIANT:
            raise serializers.ValidationError(
                {"student_user_id": "L'utilisateur doit avoir le rôle ÉTUDIANT."}
            )

        try:
            promotion = Promotion.objects.get(id=attrs["promotion_id"])
        except Promotion.DoesNotExist:
            raise serializers.ValidationError({"promotion_id": "Promotion inexistante."})

        if StudentProfile.objects.filter(user=user).exists():
            raise serializers.ValidationError(
                {"student_user_id": "Cet étudiant est déjà affecté à une promotion."}
            )

        attrs["user"] = user
        attrs["promotion"] = promotion
        return attrs

    def create(self, validated_data):
        student_profile = StudentProfile.objects.create(
            user=validated_data["user"], promotion=validated_data["promotion"]
        )
        return student_profile
    
    def to_representation(self, instance):
        """Retourner les données du StudentProfile créé"""
        return {
            "id": instance.id,
            "email": instance.user.email,
            "role": instance.user.role,
            "promotion": instance.promotion.id,
            "promotion_name": instance.promotion.name,
            "created_at": instance.created_at,
        }


class StudentProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    role = serializers.CharField(source="user.role", read_only=True)

    class Meta:
        model = StudentProfile
        fields = ["id", "email", "role", "promotion", "created_at"]

