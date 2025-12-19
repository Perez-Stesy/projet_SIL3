# Projet SIL3 - Gestion des Espaces Pédagogiques

## Description
Système de gestion des espaces pédagogiques développé avec Django (backend) et HTML/CSS/JavaScript (frontend).

## Épics développés
- **Epic 1:** Création d'un espace pédagogique vide pour une matière
- **Epic 2:** Insertion d'un formateur dans un espace pédagogique

## Structure du projet
```
projet_SIL3/
├── backend/                 # Application Django
│   ├── espaces_pedagogiques/  # Application principale
│   ├── manage.py
│   ├── settings.py
│   └── urls.py
├── frontend/               # Interface utilisateur
│   ├── index.html
│   ├── creer-espace.html
│   ├── liste-espaces.html
│   ├── ajouter-formateur.html
│   ├── creer-formateur.html
│   └── styles.css
└── requirements.txt
```

## Installation

### 1. Installer les dépendances Python
```bash
pip install -r requirements.txt
```

### 2. Créer et appliquer les migrations
```bash
cd backend
python manage.py makemigrations
python manage.py migrate
```

### 3. Créer un superutilisateur (optionnel)
```bash
python manage.py createsuperuser
```

## Utilisation

### Démarrer le serveur Django
```bash
cd backend
python manage.py runserver
```

Le serveur sera accessible sur `http://localhost:8000`

### Accéder à l'interface
Ouvrez le fichier `frontend/index.html` dans votre navigateur ou servez-le avec un serveur HTTP local.

### API Endpoints

#### Espaces Pédagogiques
- `GET /api/espaces/` - Lister tous les espaces
- `POST /api/espaces/creer/` - Créer un nouvel espace
- `GET /api/espaces/<id>/` - Détails d'un espace
- `POST /api/espaces/<id>/ajouter-formateur/` - Ajouter un formateur

#### Formateurs
- `GET /api/formateurs/` - Lister tous les formateurs
- `POST /api/formateurs/creer/` - Créer un nouveau formateur

## Technologies utilisées
- **Backend:** Django 4.2+, Django REST Framework
- **Frontend:** HTML5, CSS3, JavaScript (ES6+)
- **Base de données:** SQLite (par défaut)

## Auteur
Projet développé dans le cadre du cours SIL3 - Génie Logiciel
