"""
Commande Django pour initialiser la base de données avec des données de test
Usage: python manage.py init_data
"""
from django.core.management.base import BaseCommand
from espaces_pedagogiques.models import EspacePedagogique, Formateur


class Command(BaseCommand):
    help = 'Initialise la base de données avec des données de test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Initialisation de la base de donnees...'))
        
        # Créer des formateurs de test
        formateurs_data = [
            {
                'nom': 'Martin',
                'prenom': 'Jean',
                'email': 'jean.martin@univ.fr',
                'telephone': '+33 6 12 34 56 78'
            },
            {
                'nom': 'Dubois',
                'prenom': 'Marie',
                'email': 'marie.dubois@univ.fr',
                'telephone': '+33 6 23 45 67 89'
            },
            {
                'nom': 'Bernard',
                'prenom': 'Pierre',
                'email': 'pierre.bernard@univ.fr',
                'telephone': '+33 6 34 56 78 90'
            },
        ]
        
        formateurs_crees = []
        for formateur_data in formateurs_data:
            formateur, created = Formateur.objects.get_or_create(
                email=formateur_data['email'],
                defaults=formateur_data
            )
            if created:
                formateurs_crees.append(formateur)
                self.stdout.write(
                    self.style.SUCCESS(f'  [OK] Formateur cree: {formateur.prenom} {formateur.nom}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  [INFO] Formateur existe deja: {formateur.prenom} {formateur.nom}')
                )
        
        # Créer des espaces pédagogiques de test
        espaces_data = [
            {
                'matiere': 'Genie Logiciel',
                'code': 'GL-SIL3',
                'description': 'Cours de genie logiciel pour la troisieme annee'
            },
            {
                'matiere': 'Base de Donnees',
                'code': 'BD-SIL3',
                'description': 'Cours de base de donnees avancees'
            },
            {
                'matiere': 'Reseaux et Securite',
                'code': 'RS-SIL3',
                'description': 'Cours sur les reseaux informatiques et la securite'
            },
        ]
        
        espaces_crees = []
        for espace_data in espaces_data:
            espace, created = EspacePedagogique.objects.get_or_create(
                code=espace_data['code'],
                defaults=espace_data
            )
            if created:
                espaces_crees.append(espace)
                self.stdout.write(
                    self.style.SUCCESS(f'  [OK] Espace cree: {espace.matiere} ({espace.code})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  [INFO] Espace existe deja: {espace.matiere} ({espace.code})')
                )
        
        # Assigner des formateurs aux espaces
        if espaces_crees and formateurs_crees:
            # Assigner le premier formateur au premier espace
            if len(espaces_crees) > 0 and len(formateurs_crees) > 0:
                espaces_crees[0].formateurs.add(formateurs_crees[0])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  [OK] Formateur {formateurs_crees[0].prenom} {formateurs_crees[0].nom} '
                        f'assigne a {espaces_crees[0].matiere}'
                    )
                )
            
            # Assigner le deuxième formateur au deuxième espace
            if len(espaces_crees) > 1 and len(formateurs_crees) > 1:
                espaces_crees[1].formateurs.add(formateurs_crees[1])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  [OK] Formateur {formateurs_crees[1].prenom} {formateurs_crees[1].nom} '
                        f'assigne a {espaces_crees[1].matiere}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('\nInitialisation terminee avec succes!'))
        self.stdout.write(self.style.SUCCESS(f'Total: {Formateur.objects.count()} formateur(s) dans la base'))
        self.stdout.write(self.style.SUCCESS(f'Total: {EspacePedagogique.objects.count()} espace(s) pedagogique(s) dans la base'))

