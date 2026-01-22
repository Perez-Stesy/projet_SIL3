# 📱 QUICK START - DÉPLOIEMENT EN 5 MINUTES

## ⚡ Démarrage le plus rapide possible

### **Étape 1: Téléchargement (1 min)**
```bash
git clone https://github.com/votre-repo/plateforme-pedagogique.git
cd plateforme-pedagogique
```

### **Étape 2: Choisir votre option**

---

## 🚀 OPTION A: LOCAL (Windows) - 2 minutes

```bash
# Double-cliquez sur:
deploy-local-windows.bat

# Puis ouvrez:
# - http://localhost:5173 (Frontend)
# - http://localhost:8000 (Backend)
```

**C'est tout! ✅**

---

## 🚀 OPTION B: LOCAL (Linux/Mac) - 2 minutes

```bash
chmod +x deploy-local-linux.sh
./deploy-local-linux.sh

# Puis ouvrez:
# - http://localhost:5173 (Frontend)
# - http://localhost:8000 (Backend)
```

**C'est tout! ✅**

---

## 🐳 OPTION C: DOCKER - 5 minutes

### Prérequis:
- Docker Desktop installé (https://www.docker.com/products/docker-desktop)

### Commandes:
```bash
chmod +x deploy-docker.sh
./deploy-docker.sh

# Choisir: 1 pour développement
# Accédez à: http://localhost:3000
```

**C'est tout! ✅**

---

## ☁️ OPTION D: RAILWAY.APP - 10 minutes (Production)

### Étape 1: S'enregistrer
```
https://railway.app
```

### Étape 2: Connecter Git
```
Connecter votre compte GitHub
```

### Étape 3: Déployer
```bash
npm i -g @railway/cli
railway login
railway up
```

**Votre app est en ligne! ✅**

---

## 🔐 Identifiants par défaut

**Admin Django:**
- Email: director@example.com
- Mot de passe: (À créer via `python manage.py createsuperuser`)

**Pour créer un compte via l'interface:**
1. Enregistrez un directeur (admin)
2. Connectez-vous comme directeur
3. Créez des comptes pour formateurs et étudiants

---

## 📊 Comparaison rapide (temps vs complexité)

```
LOCAL WINDOWS    │ ⏱️  2 min   │ ⭐⭐⭐ Très facile
LOCAL LINUX      │ ⏱️  2 min   │ ⭐⭐⭐ Très facile
DOCKER           │ ⏱️  5 min   │ ⭐⭐  Facile
RAILWAY          │ ⏱️ 10 min   │ ⭐⭐  Facile (Cloud)
VPS              │ ⏱️ 30 min   │ ⭐   Intermédiaire
```

---

## ✅ Vérifier que tout marche

### Tests rapides:

**1. Backend fonctionne:**
```bash
curl http://localhost:8000/api/accounts/me/
# Vous devez voir: {"detail":"Authentication credentials were not provided."}
```

**2. Frontend charge:**
```
Ouvrez http://localhost:5173
Vous devez voir la page de connexion
```

**3. Authentification fonctionne:**
```
Inscrivez un directeur → Connectez-vous → Accédez au dashboard
```

---

## 🛑 Arrêter les services

**Local (Windows):**
- Fermer les deux fenêtres

**Local (Linux/Mac):**
```bash
Ctrl+C
```

**Docker:**
```bash
docker-compose down
```

---

## 🆘 Problèmes courants

### "Port 8000 déjà utilisé"
```bash
# Trouver et tuer le processus
lsof -i :8000
kill -9 <PID>
```

### "Python/Node pas trouvé"
- Installez Python 3.10+: https://www.python.org/
- Installez Node 18+: https://nodejs.org/

### "Docker ne démarre pas"
- Ouvrez Docker Desktop
- Attendez que le moteur démarre

---

## 📞 Besoin d'aide?

Voir le guide complet: `GUIDE_DEPLOYMENT.md`

Ou ouvrez une issue sur GitHub 🐛
