from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .permissions import IsDirector
from rest_framework.views import APIView

from .serializers import AccountActivationSerializer, UserCreateSerializer
from .serializers_read import UserListeSerializer

User = get_user_model()


class UserCreateView(generics.CreateAPIView):
    """
    Endpoint de création de comptes par le Directeur.

    - Méthode : POST
    - URL : /api/accounts/users/
    - Corps attendu : { "email": "...", "first_name": "...", "last_name": "...", "sexe": "...", "role": "FORMATEUR|ETUDIANT" }

    Couvre les cas de la User Story 1.1 :
    - Cas favorables : création de compte Formateur / Étudiant avec rôle correct
    - Cas défavorables : non authentifié, non-directeur, email invalide / existant,
      rôle non autorisé, mot de passe non conforme, erreur technique (500)
    """

    serializer_class = UserCreateSerializer
    permission_classes = [IsDirector]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        response_data = {
            "message": "Compte créé avec succès! Veuillez vérifier votre email pour activer votre compte.",
            "user": serializer.data
        }
        return Response(
            response_data,
            status=status.HTTP_201_CREATED,
            headers=headers,
        )


class UserListView(generics.ListAPIView):
    """
    Liste des utilisateurs (pour le Directeur).
    Filtre optionnel: ?role=DIRECTEUR|FORMATEUR|ETUDIANT
    """

    serializer_class = UserListeSerializer
    permission_classes = [IsDirector]

    def get_queryset(self):
        qs = User.objects.all().order_by("email")
        role = self.request.query_params.get("role")
        if role:
            qs = qs.filter(role=role)
        return qs


class MeView(generics.RetrieveAPIView):
    """
    Profil de l'utilisateur connecté (utile pour le frontend).
    """

    serializer_class = UserListeSerializer

    def get_object(self):
        return self.request.user


class AccountActivationView(APIView):
    """
    Permet à un utilisateur dont le compte a été créé par le Directeur
    de définir son mot de passe à partir de son email.
    """
    
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = AccountActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"detail": "Mot de passe défini avec succès. Vous pouvez vous connecter."})
