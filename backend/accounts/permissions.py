from rest_framework.permissions import BasePermission


class IsDirector(BasePermission):
    """
    Autorise uniquement les utilisateurs avec le rôle DIRECTEUR.
    Couvre les cas défavorables :
    - Directeur non authentifié
    - Tentative de création par un non-directeur
    """

    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "is_director", lambda: False)())


class IsTrainer(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "is_trainer", lambda: False)())


class IsStudent(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool(user and user.is_authenticated and getattr(user, "is_student", lambda: False)())


