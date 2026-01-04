# Application d'Assignation de Travaux Individuels

Application web pour assigner des travaux individuels aux étudiants. Développée avec Django (backend) et HTML/CSS/JavaScript (frontend).

## User Story

**"Assignation d'un travail individuel à un Étudiant donné"**

Cette application permet de :
- Créer et gérer des étudiants
- Assigner des travaux individuels à des étudiants
- Visualiser toutes les assignations
- Filtrer les travaux par étudiant

## Technologies Utilisées

- **Backend**: Django 5.0 + Django REST Framework
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Base de données**: SQLite (par défaut)

## Installation

### Prérequis

- Python 3.8 ou supérieur
- pip (gestionnaire de paquets Python)

### Installation

1. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   
   Sur Windows:
   ```bash
   venv\Scripts\activate
   ```
   
   Sur Linux/Mac:
   ```bash
   source venv/bin/activate
   ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

5. **Appliquer les migrations de la base de données**
   ```bash
   python manage.py migrate
   ```

6. **Créer un superutilisateur (optionnel, pour l'admin Django)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

8. **Accéder à l'application**
   - Interface principale: http://127.0.0.1:8000/
   - Interface d'administration: http://127.0.0.1:8000/admin/
   - API REST: http://127.0.0.1:8000/api/

## Structure du Projet

```
Assignation/
├── assignation_project/       # Configuration du projet Django
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── assignations/              # Application principale
│   ├── models.py              # Modèles (Etudiant, Travail)
│   ├── views.py               # Vues API REST
│   ├── serializers.py         # Sérialiseurs pour l'API
│   ├── urls.py                # URLs de l'application
│   └── admin.py               # Configuration de l'admin
├── static/                    # Fichiers statiques (CSS, JS)
│   ├── style.css
│   └── script.js
├── templates/                 # Templates Django
│   └── index.html            # Page principale
├── manage.py
├── requirements.txt
└── README.md
```

## API Endpoints

### Étudiants
- `GET /api/etudiants/` - Liste tous les étudiants
- `POST /api/etudiants/` - Créer un nouvel étudiant
- `GET /api/etudiants/{id}/` - Détails d'un étudiant
- `PUT /api/etudiants/{id}/` - Mettre à jour un étudiant
- `DELETE /api/etudiants/{id}/` - Supprimer un étudiant

### Travaux
- `GET /api/travaux/` - Liste tous les travaux
- `POST /api/travaux/` - Créer/assigner un nouveau travail
- `GET /api/travaux/{id}/` - Détails d'un travail
- `PUT /api/travaux/{id}/` - Mettre à jour un travail
- `DELETE /api/travaux/{id}/` - Supprimer un travail
- `GET /api/travaux/par_etudiant/?etudiant_id={id}` - Travaux d'un étudiant spécifique

## Utilisation

1. **Ajouter un étudiant** : Remplir le formulaire "Ajouter un Nouvel Étudiant" avec les informations requises.

2. **Assigner un travail** : 
   - Sélectionner un étudiant dans la liste déroulante
   - Remplir les informations du travail (titre, description, date limite)
   - Choisir le statut (En attente, En cours, Terminé)
   - Cliquer sur "Assigner le Travail"

3. **Visualiser les travaux** : La liste des travaux assignés s'affiche automatiquement. Vous pouvez filtrer par étudiant en utilisant le menu déroulant.

## Fonctionnalités

- ✅ Création et gestion d'étudiants
- ✅ Assignation de travaux individuels aux étudiants
- ✅ Affichage de la liste des assignations
- ✅ Filtrage des travaux par étudiant
- ✅ Interface utilisateur moderne et responsive
- ✅ API REST complète
- ✅ Interface d'administration Django

## Améliorations Futures Possibles

- Authentification utilisateur
- Upload de fichiers pour les travaux
- Notifications par email
- Tableau de bord avec statistiques
- Export des données (CSV, PDF)
- Recherche avancée

## Licence

Ce projet est un projet éducatif.
