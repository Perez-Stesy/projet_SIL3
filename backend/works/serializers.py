from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework import serializers

from accounts.models import User
from academics.models import StudentProfile
from pedagogy.models import PedagogicalSpace
from .models import Evaluation, Submission, Work, WorkAssignment

UserModel = get_user_model()


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ["id", "space", "created_by", "type", "title", "instructions", "due_at", "created_at"]
        read_only_fields = ["created_by", "created_at"]

    def validate_space(self, value: PedagogicalSpace):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        if not user or not user.is_authenticated:
            return value
        # Seuls les formateurs affectés peuvent créer un travail dans l'espace.
        if getattr(user, "role", None) == User.Roles.FORMATEUR:
            if not value.trainers.filter(id=user.id).exists():
                raise serializers.ValidationError("Formateur non affecté à cet espace.")
        return value

    def create(self, validated_data):
        request = self.context["request"]
        validated_data["created_by"] = request.user
        return super().create(validated_data)


class WorkAssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkAssignment
        fields = ["id", "work", "student", "assigned_at"]
        read_only_fields = ["assigned_at"]

    def validate(self, attrs):
        work: Work = attrs["work"]
        student: StudentProfile = attrs["student"]

        if work.type != Work.Types.INDIVIDUAL:
            raise serializers.ValidationError({"work": "Ce travail n'est pas individuel."})

        # Étudiant doit être inscrit à l'espace
        if not work.space.students.filter(id=student.id).exists():
            raise serializers.ValidationError({"student": "Étudiant non inscrit à l'espace."})

        return attrs


class StudentMyAssignmentsSerializer(serializers.ModelSerializer):
    work_title = serializers.CharField(source="work.title", read_only=True)
    work_instructions = serializers.CharField(source="work.instructions", read_only=True)
    work_due_at = serializers.DateTimeField(source="work.due_at", read_only=True)
    space_id = serializers.IntegerField(source="work.space_id", read_only=True)

    class Meta:
        model = WorkAssignment
        fields = [
            "id",
            "work",
            "work_title",
            "work_instructions",
            "work_due_at",
            "space_id",
            "assigned_at",
        ]


class SubmissionCreateSerializer(serializers.Serializer):
    """
    US 8.1: Livraison d'un travail individuel (par assignment).
    """

    assignment_id = serializers.IntegerField()
    file = serializers.FileField()

    def validate_assignment_id(self, value):
        if not WorkAssignment.objects.filter(id=value).exists():
            raise serializers.ValidationError("Travail non assigné.")
        return value

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        assignment = WorkAssignment.objects.select_related(
            "work", "student", "student__user", "work__space"
        ).get(id=attrs["assignment_id"])

        # L'étudiant ne peut livrer que ses propres assignations
        if not getattr(user, "is_student", lambda: False)():
            raise serializers.ValidationError({"detail": "Accès non autorisé."})

        if assignment.student.user_id != user.id:
            raise serializers.ValidationError({"detail": "Accès non autorisé."})

        # Double livraison interdite (OneToOne côté modèle, mais message explicite ici)
        if hasattr(assignment, "submission"):
            raise serializers.ValidationError({"detail": "Double livraison interdite."})

        # Date limite
        if assignment.work.due_at and timezone.now() > assignment.work.due_at:
            raise serializers.ValidationError({"detail": "Date dépassée."})

        attrs["assignment"] = assignment
        return attrs

    def create(self, validated_data):
        return Submission.objects.create(
            assignment=validated_data["assignment"], file=validated_data["file"]
        )


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = ["id", "assignment", "file", "submitted_at"]


class EvaluationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Evaluation
        fields = [
            "id",
            "submission",
            "evaluator",
            "grade",
            "max_grade",
            "comment",
            "published",
            "evaluated_at",
        ]
        read_only_fields = ["evaluator", "evaluated_at"]


class EvaluationCreateSerializer(serializers.Serializer):
    """
    US 9.1: évaluer un travail livré.
    """

    submission_id = serializers.IntegerField()
    grade = serializers.DecimalField(max_digits=5, decimal_places=2)
    max_grade = serializers.DecimalField(max_digits=5, decimal_places=2, default=20)
    comment = serializers.CharField(allow_blank=True, required=False)
    published = serializers.BooleanField(default=False)

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        try:
            submission = Submission.objects.select_related(
                "assignment",
                "assignment__work",
                "assignment__work__space",
            ).get(id=attrs["submission_id"])
        except Submission.DoesNotExist:
            raise serializers.ValidationError({"submission_id": "Travail non livré."})

        # Seul formateur affecté à l'espace peut évaluer
        if not getattr(user, "is_trainer", lambda: False)():
            raise serializers.ValidationError({"detail": "Accès non autorisé."})

        if not submission.assignment.work.space.trainers.filter(id=user.id).exists():
            raise serializers.ValidationError({"detail": "Formateur non autorisé."})

        if hasattr(submission, "evaluation"):
            raise serializers.ValidationError({"detail": "Déjà évalué."})

        grade = attrs["grade"]
        max_grade = attrs.get("max_grade") or 20
        if grade < 0 or grade > max_grade:
            raise serializers.ValidationError({"grade": "Note hors barème."})

        attrs["submission"] = submission
        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        return Evaluation.objects.create(
            submission=validated_data["submission"],
            evaluator=request.user,
            grade=validated_data["grade"],
            max_grade=validated_data.get("max_grade", 20),
            comment=validated_data.get("comment", ""),
            published=validated_data.get("published", False),
        )

