from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer personnalisé pour JWT qui utilise l'email au lieu du username.
    """
    
    username_field = 'email'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remplacer le champ username par email dans les champs
        if 'username' in self.fields:
            self.fields['email'] = self.fields.pop('username')
        # Définir la limite de débit si elle n'existe pas
        if 'email' not in self.fields:
            from rest_framework import serializers
            self.fields['email'] = serializers.CharField()
    
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Ajouter des informations personnalisées au token
        token['email'] = user.email
        token['role'] = user.role
        return token
    
    def validate(self, attrs):
        from rest_framework_simplejwt.exceptions import AuthenticationFailed
        
        # Récupérer l'email et le mot de passe
        email = attrs.get('email', '').strip().lower()
        password = attrs.get('password')
        
        if not email or not password:
            raise AuthenticationFailed('Email et mot de passe requis.')
        
        # Chercher l'utilisateur directement par email (insensible à la casse)
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            raise AuthenticationFailed('Aucun compte trouvé avec cet email.')
        except User.MultipleObjectsReturned:
            # En cas de doublons (ne devrait pas arriver avec unique=True)
            user = User.objects.filter(email__iexact=email).first()
        
        # Vérifier si le compte a un mot de passe utilisable
        if not user.has_usable_password():
            raise AuthenticationFailed('Ce compte n\'a pas encore été activé. Veuillez définir votre mot de passe via la page d\'activation.')
        
        # Vérifier le mot de passe
        if not user.check_password(password):
            raise AuthenticationFailed('Mot de passe incorrect.')
        
        # Vérifier si le compte est actif
        if not user.is_active:
            raise AuthenticationFailed('Ce compte utilisateur a été désactivé.')
        
        # Générer les tokens
        refresh = self.get_token(user)
        
        data = {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'role': user.role,
            'email': user.email,
        }
        
        return data
