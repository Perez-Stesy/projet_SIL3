# 🚀 DÉPLOIEMENT RAILWAY.APP - GUIDE COMPLET

## ⚡ RÉSUMÉ
- **Temps:** 10-15 minutes
- **Coût:** Gratuit (crédits Railway inclus)
- **Difficulté:** ⭐⭐ Très facile
- **Résultat:** App en ligne avec domaine custom

---

## 📋 ÉTAPE 1: S'INSCRIRE SUR RAILWAY (2 min)

### 1.1 Créer un compte
```
https://railway.app
```

### 1.2 Connecter avec GitHub
- Cliquez sur "GitHub"
- Autorisez Railway à accéder à votre GitHub
- ✅ Compte créé!

---

## 🔑 ÉTAPE 2: PRÉPARER LE PROJET (3 min)

### 2.1 Vérifier le repository Git
```bash
# Vérifier que c'est un repo Git
cd c:\Users\HP\Pictures\cursor2
git status

# Si ce n'est pas un repo, créez-en un:
git init
git add .
git commit -m "Initial commit"
```

### 2.2 Créer un nouveau repository GitHub
```
https://github.com/new
```

- **Name:** plateforme-pedagogique
- **Description:** Plateforme pédagogique (Django + React)
- **Public** ou **Private** (au choix)
- Cliquez "Create repository"

### 2.3 Pousser le code sur GitHub
```bash
cd c:\Users\HP\Pictures\cursor2

git remote add origin https://github.com/VOTRE_USERNAME/plateforme-pedagogique.git
git branch -M main
git push -u origin main
```

**✅ Code maintenant sur GitHub!**

---

## 🚂 ÉTAPE 3: DÉPLOYER AVEC RAILWAY (5 min)

### 3.1 Installer Railway CLI (Optionnel mais recommandé)
```bash
npm install -g @railway/cli
```

### 3.2 Option A: Déploiement via interface web (Plus simple)

1. Allez sur https://railway.app/dashboard
2. Cliquez sur **"New Project"**
3. Sélectionnez **"Deploy from GitHub"**
4. Autorisez Railway à accéder à votre GitHub
5. Sélectionnez votre repository: **plateforme-pedagogique**
6. Sélectionnez la branche: **main**
7. ✅ Railway crée automatiquement le déploiement!

### 3.3 Option B: Déploiement via CLI (Plus rapide)
```bash
# Se connecter
railway login

# Initialiser le projet
railway init

# Nommer le projet
# → plateforme-pedagogique

# Déployer
railway up
```

**✅ App déployée!**

---

## 🗄️ ÉTAPE 4: AJOUTER LA BASE DE DONNÉES (3 min)

### 4.1 Ajouter PostgreSQL
1. Allez sur https://railway.app/dashboard
2. Sélectionnez votre projet
3. Cliquez **"Add Service"**
4. Recherchez **"PostgreSQL"**
5. Cliquez **"Deploy"**

**✅ PostgreSQL créée et liée automatiquement!**

---

## ⚙️ ÉTAPE 5: CONFIGURER LES VARIABLES (2 min)

### 5.1 Ajouter les secrets
1. Dans le dashboard du projet
2. Cliquez sur le service **"backend"**
3. Allez dans **"Variables"**
4. Cliquez **"Raw Editor"**
5. Collez:

```env
DEBUG=False
SECRET_KEY=your-super-secret-key-change-this
ALLOWED_HOSTS=*.railway.app,localhost
DJANGO_SETTINGS_MODULE=backend.settings
```

### 5.2 Variables PostgreSQL (Automatiques)
Railway configure automatiquement:
- `DATABASE_URL`
- `DB_HOST`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`

### 5.3 Sauvegarder
Cliquez **"Save"**

**✅ Variables configurées!**

---

## 🔄 ÉTAPE 6: MIGRATIONS AUTOMATIQUES (1 min)

### 6.1 Voir les logs
```bash
# Via CLI
railway logs

# Via Dashboard: Cliquez sur "Logs"
```

### 6.2 Exécuter les migrations
```bash
# Via CLI
railway run python manage.py migrate

# Créer superuser
railway run python manage.py createsuperuser
```

**✅ Base de données configurée!**

---

## 🌐 ÉTAPE 7: ACCÉDER À VOTRE APP (30 sec)

### 7.1 Trouver votre URL
1. Dashboard Railway
2. Sélectionnez votre projet
3. Allez dans **"Deployments"**
4. Trouvez le lien public

**Exemple:** `https://plateforme-pedagogique-production.up.railway.app`

### 7.2 Accéder aux services
```
Frontend:    https://plateforme-pedagogique-production.up.railway.app
Backend:     https://plateforme-pedagogique-production.up.railway.app/api/
Admin:       https://plateforme-pedagogique-production.up.railway.app/admin/
```

**✅ Votre app est EN LIGNE!**

---

## 🎨 ÉTAPE 8: CONFIGURER DOMAINE CUSTOM (Optionnel)

### 8.1 Acheter un domaine
```
namecheap.com, godaddy.com, ou autres
```

### 8.2 Connecter le domaine
1. Dashboard Railway
2. Sélectionnez votre projet
3. Allez dans **"Domain"**
4. Cliquez **"Add Domain"**
5. Entrez: `votre-ecole.com`
6. Copiez les DNS records
7. Configurez sur votre registraire
8. Attendez 24h pour propagation

**✅ Domaine configuré!**

---

## ✅ TESTS POST-DÉPLOIEMENT

### Test 1: Frontend charge
```bash
curl https://votre-app.railway.app
# Doit retourner le HTML
```

### Test 2: API répond
```bash
curl https://votre-app.railway.app/api/accounts/me/
# Doit retourner: {"detail":"Authentication credentials were not provided."}
```

### Test 3: Admin accessible
```
https://votre-app.railway.app/admin/
# Connexion avec les identifiants créés
```

### Test 4: Authentification fonctionne
```
1. Allez sur: https://votre-app.railway.app
2. Créez un directeur (inscrivez-vous)
3. Connectez-vous
4. Accédez au dashboard
```

**✅ Tout fonctionne!**

---

## 🔍 MONITORING & LOGS

### Voir les logs en temps réel
```bash
railway logs -f
```

### Logs d'erreur
```bash
railway logs -f --service backend
```

### Redéployer
```bash
git push origin main
# Railway redéploie automatiquement (si configuré)

# Ou manuellement:
railway redeploy
```

---

## 🆘 PROBLÈMES COURANTS

### Erreur 502 Bad Gateway
```bash
# Vérifier les logs
railway logs -f

# Vérifier les migrations
railway run python manage.py migrate

# Redéployer
railway redeploy
```

### Base de données non accessible
```bash
# Vérifier la variable DATABASE_URL
railway vars

# Réinitialiser
railway run python manage.py migrate --noinput
```

### Port incorrect
```bash
# Railway utilisera le PORT 8000 par défaut
# Vérifier dans Procfile ou railway.toml

# Si erreur, ajouter:
PORT=8000
```

### CORS error
```python
# Dans backend/settings.py, ajouter:
ALLOWED_HOSTS = ['votre-app.railway.app', 'localhost']

CORS_ALLOWED_ORIGINS = [
    'https://votre-app.railway.app',
    'http://localhost:3000',
]
```

---

## 📊 COMMANDES ESSENTIELLES RAILWAY

```bash
# Authentification
railway login
railway logout

# Projet
railway init          # Créer nouveau projet
railway link          # Connecter à un projet existant
railway list          # Lister les services

# Déploiement
railway up            # Déployer
railway redeploy      # Redéployer
railway down          # Arrêter l'app

# Logs
railway logs          # Voir les logs
railway logs -f       # Logs en temps réel
railway logs --service backend

# Commandes Django
railway run python manage.py migrate
railway run python manage.py createsuperuser
railway run python manage.py collectstatic

# Variables
railway vars          # Voir toutes les variables
railway env           # Variables d'env
railway env --help    # Ajouter/modifier variables
```

---

## 🚀 DÉPLOIEMENT AUTOMATIQUE (CI/CD)

Railway redéploie **automatiquement** quand vous:

1. Poussez du code:
```bash
git add .
git commit -m "Ma modification"
git push origin main
```

2. Railway détecte le push et redéploie automatiquement ✅

---

## 💰 COÛTS

### Railway Pricing:
- **Gratuit:** $5 de crédit par mois
- **Plus:** Après épuisement des crédits
- **Calcul:** 
  - Backend: ~$2-4/mois
  - PostgreSQL: ~$1-2/mois
  - Total: ~$3-6/mois

**Pour une école: Très abordable!**

---

## 📞 SUPPORT RAILWAY

- Docs: https://docs.railway.app/
- Discord: https://railway.app/support
- Email: support@railway.app

---

## ✅ CHECKLIST FINAL

- [ ] Compte Railway créé
- [ ] Code pushé sur GitHub
- [ ] Projet créé dans Railway
- [ ] PostgreSQL ajoutée
- [ ] Variables configurées
- [ ] Migrations exécutées
- [ ] Superuser créé
- [ ] Frontend charge
- [ ] API répond
- [ ] Admin accessible
- [ ] Authentification fonctionne

**✨ Déploiement réussi! 🎉**

---

## 🎯 PROCHAINES ÉTAPES

1. ✅ Vérifier que tout fonctionne
2. 📧 Configurer Email (optionnel)
3. 🔐 Configurer SSL/HTTPS (automatique)
4. 📊 Mettre en place monitoring
5. 💾 Configurer backups quotidiens

---

**Besoin d'aide? Consultez la doc Railway: https://docs.railway.app/**
