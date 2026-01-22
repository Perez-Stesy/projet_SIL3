from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour la création de comptes par le Directeur.
    - Email unique et obligatoire
    - Rôles autorisés : FORMATEUR, ETUDIANT
    - Le mot de passe sera défini plus tard par l'utilisateur (activation de compte)
    """

    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "sexe", "role"]

    def validate_role(self, value):
        # Seuls les rôles FORMATEUR / ÉTUDIANT peuvent être créés via cette fonctionnalité
        allowed = {User.Roles.FORMATEUR, User.Roles.ETUDIANT}
        if value not in allowed:
            raise serializers.ValidationError(
                "Rôle non autorisé. Seuls FORMATEUR et ÉTUDIANT peuvent être créés."
            )
        return value

    def create(self, validated_data):
        user = User(**validated_data)
        # Aucun mot de passe défini ici : l'utilisateur devra activer son compte.
        user.set_unusable_password()
        user.full_clean()
        user.save()
        return user


class AccountActivationSerializer(serializers.Serializer):
    """
    Activation de compte par l'utilisateur :
    - Fournit son email
    - Définit son mot de passe (une seule fois)
    """

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirmation = serializers.CharField(write_only=True, min_length=8)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirmation"]:
            raise serializers.ValidationError(
                {"password_confirmation": "Les mots de passe ne correspondent pas."}
            )
        try:
            user = User.objects.get(email=attrs["email"])
        except User.DoesNotExist:
            raise serializers.ValidationError({"email": "Aucun compte avec cet e-mail."})

        if user.has_usable_password():
            raise serializers.ValidationError(
                {"email": "Ce compte est déjà activé. Veuillez vous connecter."}
            )

        attrs["user"] = user
        return attrs

    def save(self, **kwargs):
        user = self.validated_data["user"]
        user.set_password(self.validated_data["password"])
        user.save()
        return user
