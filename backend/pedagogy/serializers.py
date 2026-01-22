from django.contrib.auth import get_user_model
from rest_framework import serializers

from accounts.models import User
from academics.models import StudentProfile, Subject
from .models import PedagogicalSpace

UserModel = get_user_model()


class PedagogicalSpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PedagogicalSpace
        fields = [
            "id",
            "subject",
            "year",
            "promotion",
            "trainers",
            "students",
            "created_at",
        ]
        read_only_fields = ["trainers", "students", "created_at"]

    def validate(self, attrs):
        # cohérence simple: l'année de l'espace doit correspondre à l'année de la promotion
        promotion = attrs.get("promotion")
        year = attrs.get("year")
        if promotion and year and promotion.year != year:
            raise serializers.ValidationError(
                {"year": "L'année doit correspondre à l'année de la promotion."}
            )
        # matière existante est déjà garantie via FK
        return attrs


class AssignTrainerSerializer(serializers.Serializer):
    """
    US 3.2: affecter un formateur à un espace.
    """

    trainer_user_id = serializers.IntegerField()

    def validate_trainer_user_id(self, value):
        try:
            user = UserModel.objects.get(id=value)
        except UserModel.DoesNotExist:
            raise serializers.ValidationError("Formateur inexistant.")
        if getattr(user, "role", None) != User.Roles.FORMATEUR:
            raise serializers.ValidationError("L'utilisateur doit avoir le rôle FORMATEUR.")
        return value


class AddStudentToSpaceSerializer(serializers.Serializer):
    """
    US 3.3: ajouter un étudiant à un espace (doit appartenir à la promotion).
    """

    student_profile_id = serializers.IntegerField()

    def validate_student_profile_id(self, value):
        if not StudentProfile.objects.filter(id=value).exists():
            raise serializers.ValidationError("Étudiant inexistant.")
        return value


class SpaceDetailSerializer(serializers.ModelSerializer):
    subject_code = serializers.CharField(source="subject.code", read_only=True)
    subject_name = serializers.CharField(source="subject.name", read_only=True)
    promotion_name = serializers.CharField(source="promotion.name", read_only=True)
    promotion_year = serializers.IntegerField(source="promotion.year", read_only=True)

    trainer_emails = serializers.SerializerMethodField()
    student_emails = serializers.SerializerMethodField()
    students_details = serializers.SerializerMethodField()

    class Meta:
        model = PedagogicalSpace
        fields = [
            "id",
            "subject",
            "subject_code",
            "subject_name",
            "year",
            "promotion",
            "promotion_name",
            "promotion_year",
            "trainers",
            "trainer_emails",
            "students",
            "student_emails",
            "students_details",
            "created_at",
        ]

    def get_trainer_emails(self, obj):
        return list(obj.trainers.values_list("email", flat=True))

    def get_student_emails(self, obj):
        return list(obj.students.values_list("user__email", flat=True))

    def get_students_details(self, obj):
        return list(obj.students.values("id", "user__email"))

