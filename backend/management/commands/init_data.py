"""
Commande Django pour initialiser la base de données avec des données de test
Usage: python manage.py init_data
"""
from django.core.management.base import BaseCommand
from espaces_pedagogiques.models import EspacePedagogique, Formateur


class Command(BaseCommand):
    help = 'Initialise la base de données avec des données de test'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🚀 Initialisation de la base de données...'))
        
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
                    self.style.SUCCESS(f'  ✅ Formateur créé: {formateur.prenom} {formateur.nom}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠️  Formateur existe déjà: {formateur.prenom} {formateur.nom}')
                )
        
        # Créer des espaces pédagogiques de test
        espaces_data = [
            {
                'matiere': 'Génie Logiciel',
                'code': 'GL-SIL3',
                'description': 'Cours de génie logiciel pour la troisième année'
            },
            {
                'matiere': 'Base de Données',
                'code': 'BD-SIL3',
                'description': 'Cours de base de données avancées'
            },
            {
                'matiere': 'Réseaux et Sécurité',
                'code': 'RS-SIL3',
                'description': 'Cours sur les réseaux informatiques et la sécurité'
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
                    self.style.SUCCESS(f'  ✅ Espace créé: {espace.matiere} ({espace.code})')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'  ⚠️  Espace existe déjà: {espace.matiere} ({espace.code})')
                )
        
        # Assigner des formateurs aux espaces
        if espaces_crees and formateurs_crees:
            # Assigner le premier formateur au premier espace
            if len(espaces_crees) > 0 and len(formateurs_crees) > 0:
                espaces_crees[0].formateurs.add(formateurs_crees[0])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✅ Formateur {formateurs_crees[0].prenom} {formateurs_crees[0].nom} '
                        f'assigné à {espaces_crees[0].matiere}'
                    )
                )
            
            # Assigner le deuxième formateur au deuxième espace
            if len(espaces_crees) > 1 and len(formateurs_crees) > 1:
                espaces_crees[1].formateurs.add(formateurs_crees[1])
                self.stdout.write(
                    self.style.SUCCESS(
                        f'  ✅ Formateur {formateurs_crees[1].prenom} {formateurs_crees[1].nom} '
                        f'assigné à {espaces_crees[1].matiere}'
                    )
                )
        
        self.stdout.write(self.style.SUCCESS('\n✨ Initialisation terminée avec succès!'))
        self.stdout.write(self.style.SUCCESS(f'📊 {Formateur.objects.count()} formateur(s) dans la base'))
        self.stdout.write(self.style.SUCCESS(f'📚 {EspacePedagogique.objects.count()} espace(s) pédagogique(s) dans la base'))

