"""
Script pour vérifier et corriger le rôle d'un utilisateur dans la base de données.
Usage: python manage.py shell < check_user_role.py
Ou: python manage.py shell puis copier-coller le contenu
"""

from accounts.models import User

# Afficher tous les utilisateurs et leurs rôles
print("=== LISTE DES UTILISATEURS ===")
for user in User.objects.all():
    print(f"ID: {user.id}")
    print(f"Email: {user.email}")
    print(f"Username: {user.username}")
    print(f"Rôle: {user.role}")
    print(f"Superuser: {user.is_superuser}")
    print(f"Actif: {user.is_active}")
    print("-" * 40)

# Vérifier/corriger un utilisateur spécifique
email = input("\nEntrez l'email de l'utilisateur à vérifier/corriger (ou appuyez sur Entrée pour quitter): ")

if email:
    try:
        user = User.objects.get(email=email)
        print(f"\nUtilisateur trouvé: {user.email}")
        print(f"Rôle actuel: {user.role}")
        print(f"Superuser: {user.is_superuser}")
        
        # Si c'est un superuser, s'assurer qu'il est DIRECTEUR
        if user.is_superuser and user.role != User.Roles.DIRECTEUR:
            print(f"\n⚠️  Superuser détecté mais rôle = {user.role}")
            print("Correction automatique en cours...")
            user.role = User.Roles.DIRECTEUR
            user.save()
            print(f"✅ Rôle corrigé à: {user.role}")
        elif not user.is_superuser and user.role == User.Roles.DIRECTEUR:
            print(f"\n⚠️  Utilisateur DIRECTEUR mais pas superuser")
            print("Voulez-vous le définir comme superuser? (o/n): ", end="")
            response = input().lower()
            if response == 'o':
                user.is_superuser = True
                user.save()
                print("✅ Utilisateur défini comme superuser")
        
        print(f"\nÉtat final:")
        print(f"Email: {user.email}")
        print(f"Rôle: {user.role}")
        print(f"Superuser: {user.is_superuser}")
        
    except User.DoesNotExist:
        print(f"❌ Aucun utilisateur trouvé avec l'email: {email}")
