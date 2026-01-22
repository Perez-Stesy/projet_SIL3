# 🖥️ Commandes manuelles pour lancer les serveurs

## 📍 Prérequis

Vérifiez d'abord que vous avez :
- Python installé : `python --version`
- Node.js installé : `node --version`
- npm installé : `npm --version`

---

## 🔵 BACKEND (Django)

### Étape 1 : Ouvrir un terminal PowerShell ou CMD

### Étape 2 : Aller dans le dossier backend
```powershell
cd backend
```

### Étape 3 : Activer l'environnement virtuel (si vous utilisez venv)
```powershell
# Si vous êtes à la racine du projet
..\venv\Scripts\activate

# OU si vous êtes déjà dans backend/
..\..\venv\Scripts\activate
```

**Note :** Si vous n'avez pas d'environnement virtuel, vous pouvez installer les packages globalement (non recommandé).

### Étape 4 : Installer les dépendances Python
```powershell
pip install -r ..\requirements.txt
```

### Étape 5 : Créer le fichier .env (si nécessaire)
```powershell
# Vérifier si .env existe
dir .env

# Si .env n'existe pas, créer depuis .env.example (si disponible)
copy .env.example .env
```

**Contenu minimal du fichier `.env` :**
```
SECRET_KEY=django-insecure-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
USE_POSTGRESQL=false
```

### Étape 6 : Appliquer les migrations
```powershell
python manage.py migrate
```

### Étape 7 : Lancer le serveur Django
```powershell
python manage.py runserver
```

**✅ Le backend sera disponible sur : http://127.0.0.1:8000**

---

## 🟢 FRONTEND (React/Vite)

### Étape 1 : Ouvrir un NOUVEAU terminal PowerShell ou CMD
*(Gardez le terminal du backend ouvert)*

### Étape 2 : Aller dans le dossier frontend
```powershell
cd frontend
```

### Étape 3 : Installer les dépendances npm (première fois seulement)
```powershell
npm install
```

**Note :** Cette étape peut prendre quelques minutes la première fois.

### Étape 4 : Lancer le serveur de développement
```powershell
npm run dev
```

**✅ Le frontend sera disponible sur : http://localhost:5173**

---

## 📋 RÉSUMÉ DES COMMANDES

### Backend (dans un terminal)
```powershell
cd backend
..\venv\Scripts\activate
pip install -r ..\requirements.txt
python manage.py migrate
python manage.py runserver
```

### Frontend (dans un autre terminal)
```powershell
cd frontend
npm install
npm run dev
```

---

## 🔧 COMMANDES UTILES

### Créer un superutilisateur (Directeur)
```powershell
cd backend
..\venv\Scripts\activate
python manage.py createsuperuser
```

### Vérifier que le backend fonctionne
Ouvrez dans votre navigateur : http://127.0.0.1:8000/admin

### Vérifier que le frontend fonctionne
Ouvrez dans votre navigateur : http://localhost:5173

### Arrêter les serveurs
- Appuyez sur `Ctrl + C` dans chaque terminal

---

## 🐛 DÉPANNAGE

### Erreur : "python n'est pas reconnu"
```powershell
# Essayez avec py au lieu de python
py --version
py manage.py runserver
```

### Erreur : "pip n'est pas reconnu"
```powershell
# Essayez avec python -m pip
python -m pip install -r ..\requirements.txt
```

### Erreur : "node n'est pas reconnu"
- Installez Node.js depuis https://nodejs.org/
- Redémarrez le terminal après l'installation

### Erreur : "Port déjà utilisé"
```powershell
# Pour le backend, utilisez un autre port
python manage.py runserver 8001

# Pour le frontend, modifiez vite.config.js ou utilisez
npm run dev -- --port 5174
```

### Erreur : "Module non trouvé" (Python)
```powershell
# Réinstaller les dépendances
pip install -r ..\requirements.txt --force-reinstall
```

### Erreur : "Module non trouvé" (Node.js)
```powershell
# Supprimer node_modules et réinstaller
rmdir /s /q node_modules
npm install
```

### Erreur : "Migration nécessaire"
```powershell
cd backend
python manage.py migrate
```

### Erreur : "Base de données verrouillée" (SQLite)
- Fermez tous les terminaux qui utilisent la base de données
- Redémarrez le serveur

---

## 📝 NOTES IMPORTANTES

1. **Deux terminaux nécessaires** : Un pour le backend, un pour le frontend
2. **Gardez les deux terminaux ouverts** pendant que vous travaillez
3. **L'ordre de démarrage n'est pas important**, mais le backend doit être démarré avant d'utiliser l'application
4. **Pour arrêter** : Appuyez sur `Ctrl + C` dans chaque terminal

---

## ✅ VÉRIFICATION FINALE

Une fois les deux serveurs lancés :

1. ✅ Backend : http://127.0.0.1:8000/admin (doit afficher la page de connexion Django)
2. ✅ Frontend : http://localhost:5173 (doit afficher l'interface de l'application)
3. ✅ API : http://127.0.0.1:8000/api (peut retourner une erreur d'authentification, c'est normal)

---

## 🎯 COMMANDES RAPIDES (Copier-Coller)

### Terminal 1 - Backend
```powershell
cd C:\Users\OBE\Music\cursor2\backend
..\venv\Scripts\activate
pip install -r ..\requirements.txt
python manage.py migrate
python manage.py runserver
```

### Terminal 2 - Frontend
```powershell
cd C:\Users\OBE\Music\cursor2\frontend
npm install
npm run dev
```
