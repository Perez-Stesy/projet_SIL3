# Plateforme Pédagogique

Application web de gestion pédagogique avec Django (Backend) et React (Frontend).

## 🚀 Démarrage Rapide

### Prérequis

- Python 3.10+
- Node.js 18+
- PostgreSQL 12+

### 1. Configuration PostgreSQL

#### Installation PostgreSQL

**Windows:**
- Téléchargez depuis https://www.postgresql.org/download/windows/
- Installez avec les paramètres par défaut
- Notez le mot de passe du superutilisateur `postgres`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

#### Création de la base de données

```bash
# Connectez-vous à PostgreSQL
psql -U postgres

# Dans psql, créez la base de données
CREATE DATABASE plateforme_pedagogique;

# Quittez psql
\q
```

### 2. Configuration Backend

1. **Créez un fichier `.env` dans le répertoire `backend/`:**

```env
DB_NAME=plateforme_pedagogique
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe_postgres
DB_HOST=localhost
DB_PORT=5432
```

2. **Installez les dépendances Python:**

```bash
cd backend
pip install -r ../requirements.txt
```

3. **Appliquez les migrations:**

```bash
python manage.py migrate
```

4. **Créez un superutilisateur (optionnel):**

```bash
python manage.py createsuperuser
```

5. **Lancez le serveur backend:**

```bash
# Windows
start.bat

# Linux/macOS
python manage.py runserver
```

Le backend sera accessible sur `http://127.0.0.1:8000`

### 3. Configuration Frontend

1. **Installez les dépendances:**

```bash
cd frontend
npm install
```

2. **Lancez le serveur de développement:**

```bash
# Windows
start.bat

# Linux/macOS
npm run dev
```

Le frontend sera accessible sur `http://localhost:5173` (ou le port indiqué)

## 📁 Structure du Projet

```
├── backend/          # API Django REST Framework
│   ├── accounts/     # Gestion des utilisateurs
│   ├── academics/    # Promotions, matières, profils étudiants
│   ├── pedagogy/     # Espaces pédagogiques
│   └── works/        # Travaux, assignations, livraisons, évaluations
├── frontend/         # Application React
│   └── src/
│       ├── pages/    # Pages principales
│       ├── components/  # Composants réutilisables
│       └── services/    # Services API
└── requirements.txt  # Dépendances Python
```

## 🎨 Fonctionnalités

### Directeur
- Création de comptes (Formateurs, Étudiants)
- Gestion des promotions
- Gestion des matières
- Création d'espaces pédagogiques
- Affectation d'étudiants aux promotions
- Affectation de formateurs aux espaces
- Ajout d'étudiants aux espaces

### Formateur
- Création de travaux (individuels/collectifs)
- Assignation de travaux aux étudiants
- Évaluation des livraisons
- Consultation du classement

### Étudiant
- Consultation des travaux assignés
- Livraison de travaux
- Consultation des évaluations
- Consultation du classement

## 🛠️ Technologies Utilisées

### Backend
- Django 5.2.10
- Django REST Framework
- PostgreSQL
- JWT Authentication

### Frontend
- React 19.2.0
- React Router DOM
- Axios
- React Icons
- Vite

## 📝 Notes

- Assurez-vous que PostgreSQL est démarré avant de lancer le backend
- Le fichier `.env` doit être créé dans le répertoire `backend/` avec vos identifiants PostgreSQL
- En cas d'erreur de connexion à la base de données, vérifiez vos identifiants dans le fichier `.env`

## 🐛 Dépannage

### Erreur de connexion PostgreSQL
- Vérifiez que PostgreSQL est démarré
- Vérifiez les identifiants dans le fichier `.env`
- Vérifiez que la base de données `plateforme_pedagogique` existe

### Erreur de migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Erreur de dépendances
```bash
pip install -r requirements.txt
npm install
```
