# Application de Consultation des Travaux Assignés

Application web pour consulter les travaux assignés à un étudiant donné.

## Technologies utilisées

- **Backend**: Django 4.2+
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Base de données**: SQLite (par défaut)

## Installation

### Prérequis

- **Python 3.8 ou supérieur** - [Télécharger Python](https://www.python.org/downloads/)
  - ⚠️ **IMPORTANT** : Lors de l'installation, cochez la case **"Add Python to PATH"**
- pip (gestionnaire de paquets Python) - inclus avec Python

### Installation rapide (Windows)

1. **Installer Python** si ce n'est pas déjà fait :
   - Téléchargez depuis https://www.python.org/downloads/
   - ⚠️ **Cochez "Add Python to PATH"** lors de l'installation
   - Redémarrez votre terminal après l'installation

2. **Exécuter le script de démarrage** :
   - Double-cliquez sur `start.bat` (ou `start.ps1` dans PowerShell)
   - Le script installera automatiquement les dépendances et créera la base de données

### Étapes d'installation manuelle

1. **Cloner ou télécharger le projet**

2. **Créer un environnement virtuel (recommandé)**
   ```bash
   python -m venv venv
   ```

3. **Activer l'environnement virtuel**
   - Sur Windows:
     ```bash
     venv\Scripts\activate
     ```
   - Sur Linux/Mac:
     ```bash
     source venv/bin/activate
     ```

4. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

5. **Effectuer les migrations de la base de données**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Créer un superutilisateur (optionnel, pour accéder à l'admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Créer des données d'exemple (optionnel)**
   ```bash
   python manage.py create_sample_data
   ```
   Cela créera 3 étudiants avec des travaux assignés pour tester l'application.

8. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

9. **Accéder à l'application**
   - Interface principale: http://127.0.0.1:8000/
   - Interface d'administration: http://127.0.0.1:8000/admin/

## Utilisation

### Interface principale

1. Entrez le numéro d'étudiant dans le champ de recherche, ou
2. Sélectionnez un étudiant dans la liste déroulante
3. Cliquez sur "Rechercher" ou sélectionnez un étudiant
4. Les travaux assignés à l'étudiant s'afficheront avec leurs détails

### Interface d'administration

Accédez à `/admin/` pour:
- Ajouter des étudiants
- Assigner des travaux aux étudiants
- Modifier les statuts des travaux
- Ajouter des notes et commentaires

## Structure du projet

```
consultation/
├── consultation/          # Configuration du projet Django
│   ├── settings.py       # Paramètres Django
│   ├── urls.py           # URLs principales
│   └── wsgi.py           # Configuration WSGI
├── travaux/              # Application principale
│   ├── models.py         # Modèles Etudiant et Travail
│   ├── views.py          # Vues API
│   ├── urls.py           # URLs de l'application
│   └── admin.py          # Configuration admin
├── templates/            # Templates HTML
│   └── index.html        # Page principale
├── static/               # Fichiers statiques
│   ├── css/
│   │   └── style.css     # Styles CSS
│   └── js/
│       └── main.js       # JavaScript
├── manage.py             # Script de gestion Django
└── requirements.txt      # Dépendances Python
```

## API Endpoints

- `GET /api/etudiants/` - Liste de tous les étudiants
- `GET /api/etudiants/<id>/travaux/` - Travaux d'un étudiant par ID
- `GET /api/etudiants/<numero>/travaux/` - Travaux d'un étudiant par numéro

## Modèles de données

### Etudiant
- nom, prenom, email, numero_etudiant, date_inscription

### Travail
- titre, description, etudiant (FK), date_assignation, date_limite, statut, note, commentaire

## Statuts des travaux

- **En attente**: Travail assigné mais pas encore commencé
- **En cours**: Travail en cours de réalisation
- **Terminé**: Travail complété
- **En retard**: Date limite dépassée

## Développement

Pour ajouter des données de test, utilisez l'interface d'administration Django ou créez un script de migration de données.

## Licence

Ce projet est fourni à des fins éducatives.

