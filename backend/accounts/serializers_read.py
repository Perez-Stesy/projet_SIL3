from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserListeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "sexe", "role", "is_active", "is_superuser"]

