"""
Commande Django pour créer des données d'exemple
Usage: python manage.py create_sample_data
"""
from django.core.management.base import BaseCommand
from datetime import date, timedelta
from travaux.models import Etudiant, Travail


class Command(BaseCommand):
    help = 'Crée des données d\'exemple (étudiants et travaux)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Création des données d\'exemple...'))
        
        # Créer des étudiants
        etudiant1 = Etudiant.objects.create(
            nom='Dupont',
            prenom='Jean',
            email='jean.dupont@example.com',
            numero_etudiant='ETU001'
        )
        
        etudiant2 = Etudiant.objects.create(
            nom='Martin',
            prenom='Marie',
            email='marie.martin@example.com',
            numero_etudiant='ETU002'
        )
        
        etudiant3 = Etudiant.objects.create(
            nom='Bernard',
            prenom='Pierre',
            email='pierre.bernard@example.com',
            numero_etudiant='ETU003'
        )
        
        # Créer des travaux pour l'étudiant 1
        Travail.objects.create(
            titre='Projet de développement web',
            description='Créer une application web moderne avec Django et React. Le projet doit inclure une authentification utilisateur et une API REST.',
            etudiant=etudiant1,
            date_limite=date.today() + timedelta(days=30),
            statut='en_cours'
        )
        
        Travail.objects.create(
            titre='Rapport sur les bases de données',
            description='Rédiger un rapport de 20 pages sur les systèmes de gestion de bases de données relationnelles et NoSQL.',
            etudiant=etudiant1,
            date_limite=date.today() + timedelta(days=15),
            statut='en_attente'
        )
        
        Travail.objects.create(
            titre='Examen de mathématiques',
            description='Examen final de mathématiques appliquées. Durée: 2 heures.',
            etudiant=etudiant1,
            date_limite=date.today() - timedelta(days=5),
            statut='termine',
            note=16.5,
            commentaire='Excellent travail. Bonne compréhension des concepts.'
        )
        
        # Créer des travaux pour l'étudiant 2
        Travail.objects.create(
            titre='Projet de machine learning',
            description='Implémenter un modèle de classification d\'images en utilisant TensorFlow.',
            etudiant=etudiant2,
            date_limite=date.today() + timedelta(days=45),
            statut='en_cours'
        )
        
        Travail.objects.create(
            titre='Devoir de programmation Python',
            description='Résoudre 10 exercices de programmation en Python sur les structures de données.',
            etudiant=etudiant2,
            date_limite=date.today() - timedelta(days=10),
            statut='en_retard'
        )
        
        # Créer des travaux pour l'étudiant 3
        Travail.objects.create(
            titre='Présentation sur la cybersécurité',
            description='Préparer et présenter un exposé de 15 minutes sur les enjeux de la cybersécurité moderne.',
            etudiant=etudiant3,
            date_limite=date.today() + timedelta(days=7),
            statut='en_attente'
        )
        
        Travail.objects.create(
            titre='TP de réseaux',
            description='Configuration d\'un réseau local avec routeurs et switches. Rapport à rendre.',
            etudiant=etudiant3,
            date_limite=date.today() - timedelta(days=2),
            statut='termine',
            note=14.0,
            commentaire='Bon travail, quelques améliorations possibles sur la documentation.'
        )
        
        self.stdout.write(self.style.SUCCESS(
            f'✓ Créé {Etudiant.objects.count()} étudiants'
        ))
        self.stdout.write(self.style.SUCCESS(
            f'✓ Créé {Travail.objects.count()} travaux'
        ))
        self.stdout.write(self.style.SUCCESS('\nDonnées d\'exemple créées avec succès!'))
        self.stdout.write(self.style.WARNING(
            '\nVous pouvez maintenant tester l\'application avec les numéros d\'étudiants:'
        ))
        self.stdout.write('  - ETU001 (Jean Dupont)')
        self.stdout.write('  - ETU002 (Marie Martin)')
        self.stdout.write('  - ETU003 (Pierre Bernard)')


