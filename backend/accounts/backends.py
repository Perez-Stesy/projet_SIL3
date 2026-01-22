"""
Backend d'authentification personnalisé pour utiliser l'email au lieu du username.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

User = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authentifie les utilisateurs avec leur email au lieu du username.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        # Si username est fourni, essayer de l'utiliser comme email
        email = kwargs.get('email', username)
        
        if email is None or password is None:
            return None
        
        try:
            # Chercher l'utilisateur par email
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            # Retourner None pour déclencher le backend suivant
            return None
        
        # Vérifier le mot de passe
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        
        return None
