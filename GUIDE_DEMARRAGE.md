# 🚀 Guide de démarrage - Plateforme Pédagogique

Ce guide vous explique comment lancer le backend et le frontend de l'application.

## 📋 Prérequis

Avant de commencer, assurez-vous d'avoir installé :

1. **Python 3.11 ou supérieur**
   - Télécharger depuis : https://www.python.org/downloads/
   - Vérifier l'installation : `python --version`

2. **Node.js 18 ou supérieur**
   - Télécharger depuis : https://nodejs.org/
   - Vérifier l'installation : `node --version` et `npm --version`

3. **PostgreSQL (optionnel, SQLite sera utilisé par défaut)**
   - Si vous utilisez PostgreSQL, installez-le depuis : https://www.postgresql.org/download/

## 🎯 Démarrage rapide

### Option 1 : Lancer les deux services en même temps (Recommandé)

Double-cliquez sur le fichier **`start-all.bat`** à la racine du projet.

Cela ouvrira deux fenêtres :
- Une pour le backend (Django)
- Une pour le frontend (React/Vite)

### Option 2 : Lancer séparément

#### Backend (Django)

1. Ouvrir un terminal dans le dossier `backend`
2. Double-cliquer sur **`start.bat`** OU exécuter :
   ```bash
   cd backend
   start.bat
   ```

Le backend sera disponible sur : **http://127.0.0.1:8000**

#### Frontend (React)

1. Ouvrir un **nouveau** terminal dans le dossier `frontend`
2. Double-cliquer sur **`start.bat`** OU exécuter :
   ```bash
   cd frontend
   start.bat
   ```

Le frontend sera disponible sur : **http://localhost:5173**

## ⚙️ Configuration initiale

### 1. Configuration du backend

Le fichier `backend/.env` est nécessaire. S'il n'existe pas, il sera créé automatiquement depuis `backend/.env.example`.

**Variables importantes :**
- `SECRET_KEY` : Clé secrète Django (générée automatiquement si absente)
- `DEBUG` : `True` pour le développement, `False` pour la production
- `ALLOWED_HOSTS` : `localhost,127.0.0.1` pour le développement

**Pour PostgreSQL (optionnel) :**
```env
USE_POSTGRESQL=true
DB_NAME=plateforme_pedagogique
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

### 2. Créer un superutilisateur (Directeur)

Une fois le backend démarré, dans un nouveau terminal :

```bash
cd backend
python manage.py createsuperuser
```

Suivez les instructions pour créer un compte Directeur.

## 🔍 Vérification

### Vérifier que le backend fonctionne

Ouvrez votre navigateur et allez sur :
- **http://127.0.0.1:8000/admin** - Interface d'administration Django
- **http://127.0.0.1:8000/api** - API REST

### Vérifier que le frontend fonctionne

Ouvrez votre navigateur et allez sur :
- **http://localhost:5173** - Interface utilisateur

## 🐛 Dépannage

### Erreur : "Python n'est pas installé"

1. Installez Python depuis https://www.python.org/downloads/
2. Cochez "Add Python to PATH" lors de l'installation
3. Redémarrez votre terminal

### Erreur : "Node.js n'est pas installé"

1. Installez Node.js depuis https://nodejs.org/
2. Redémarrez votre terminal

### Erreur : "Module non trouvé" (Python)

```bash
cd backend
pip install -r ../requirements.txt
```

### Erreur : "Module non trouvé" (Node.js)

```bash
cd frontend
npm install
```

### Erreur : "Port déjà utilisé"

**Backend (port 8000) :**
- Fermez l'application qui utilise le port 8000
- OU modifiez le port dans `backend/start.bat` : `python manage.py runserver 8001`

**Frontend (port 5173) :**
- Fermez l'application qui utilise le port 5173
- OU modifiez le port dans `frontend/vite.config.js`

### Erreur de connexion à la base de données

**Si vous utilisez SQLite (par défaut) :**
- Aucune configuration nécessaire, cela fonctionne automatiquement

**Si vous utilisez PostgreSQL :**
1. Vérifiez que PostgreSQL est démarré
2. Vérifiez les informations dans `backend/.env`
3. Créez la base de données : `createdb plateforme_pedagogique`

### Erreur : "Migration nécessaire"

```bash
cd backend
python manage.py migrate
```

## 📝 Commandes utiles

### Backend

```bash
# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Créer un shell Django
python manage.py shell

# Collecter les fichiers statiques
python manage.py collectstatic
```

### Frontend

```bash
# Installer les dépendances
npm install

# Lancer en mode développement
npm run dev

# Construire pour la production
npm run build

# Prévisualiser la version de production
npm run preview
```

## 🎓 Première utilisation

1. **Créer un compte Directeur** via `python manage.py createsuperuser`
2. **Se connecter** à l'interface admin : http://127.0.0.1:8000/admin
3. **Créer des comptes** pour les formateurs et étudiants via l'interface admin
4. **Activer les comptes** via la page d'activation : http://localhost:5173/activation
5. **Se connecter** via la page de connexion : http://localhost:5173/connexion

## 📞 Support

Si vous rencontrez des problèmes :

1. Vérifiez les logs dans les fenêtres du backend et frontend
2. Consultez le fichier `README_DEPLOY.md` pour plus d'informations
3. Vérifiez que tous les prérequis sont installés correctement

## 🚀 Prochaines étapes

Une fois l'application lancée :

1. ✅ Testez la connexion avec un compte activé
2. ✅ Explorez les différentes fonctionnalités selon votre rôle
3. ✅ Consultez `DEPLOY.md` pour déployer en production
