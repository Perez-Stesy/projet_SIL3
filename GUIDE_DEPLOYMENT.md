# 🚀 GUIDE DE DÉPLOIEMENT - PLATEFORME PÉDAGOGIQUE

## 📋 OPTIONS DE DÉPLOIEMENT (du plus simple au plus robuste)

### **OPTION 1: DÉPLOIEMENT LOCAL (Développement rapide) ⭐ LE PLUS SIMPLE**
**Temps:** 2-3 minutes | **Difficulté:** ⭐ Très facile

```bash
# Windows
./deploy-local-windows.bat

# Linux/Mac
chmod +x deploy-local-linux.sh
./deploy-local-linux.sh
```

**Avantages:**
- ✅ Démarrage ultra-rapide
- ✅ Idéal pour tester localement
- ✅ Pas besoin de Docker
- ✅ Base de données SQLite incluse

**URL d'accès:**
- Frontend: http://localhost:5173
- Backend: http://localhost:8000
- Admin: http://localhost:8000/admin

---

### **OPTION 2: DOCKER COMPOSE (Production simple) ⭐ RECOMMANDÉ**
**Temps:** 5-10 minutes | **Difficulté:** ⭐⭐ Facile

```bash
# Démarrer tout avec Docker
docker-compose up -d

# Voir les logs
docker-compose logs -f

# Arrêter
docker-compose down
```

**Avantages:**
- ✅ Production-ready
- ✅ Base PostgreSQL persistante
- ✅ Isolation complète
- ✅ Scaling facile
- ✅ Même environnement que la prod

**Configuration requise:**
- Docker Desktop installé
- 4GB RAM libre

**URL d'accès:**
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- DB: localhost:5432

---

### **OPTION 3: CLOUD DEPLOYMENT (Heroku/Railway) ⭐⭐ TRÈS SIMPLE**
**Temps:** 10-15 minutes | **Difficulté:** ⭐⭐ Facile

#### Sur **Railway.app** (Plus facile):
```bash
# 1. Créer compte sur railway.app
# 2. Installer Railway CLI
npm i -g @railway/cli

# 3. Déployer
railway login
railway init
railway up
```

#### Sur **Heroku** (Clasique):
```bash
heroku login
git push heroku main
```

**Avantages:**
- ✅ Déploiement en un clic
- ✅ HTTPS automatique
- ✅ Domaine custom possible
- ✅ Gratuit (Railway avec crédits)
- ✅ PostgreSQL géré

---

### **OPTION 4: VPS/SERVEUR DÉDIÉ (Production robuste) ⭐⭐⭐ PROFESSIONNEL**
**Temps:** 20-30 minutes | **Difficulté:** ⭐⭐⭐ Intermédiaire

Exemple avec DigitalOcean/Linode:
```bash
# SSH sur le serveur
ssh root@votre_ip

# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Cloner le projet
git clone votre_repo
cd votre_repo

# Déployer
docker-compose -f docker-compose.prod.yml up -d

# Setup SSL avec Certbot
sudo apt install certbot python3-certbot-nginx
sudo certbot certonly --standalone -d votre_domaine.com
```

**Avantages:**
- ✅ Performance maximale
- ✅ Contrôle total
- ✅ Scalabilité illimitée
- ✅ Backup custom
- ✅ Coût ~5-20$/mois

---

## 🎯 RECOMMANDATION PAR CAS D'USAGE

| Cas d'usage | Option recommandée |
|---|---|
| Tester localement rapidement | **Option 1** (Local) |
| Dev en équipe / tests | **Option 2** (Docker) |
| MVP / Prototype en ligne | **Option 3** (Railway) |
| Production pour école | **Option 4** (VPS) |

---

## 🔧 PRÉ-REQUIS SELON L'OPTION

### Option 1: Local
- ✅ Python 3.10+
- ✅ Node.js 18+
- ✅ Git

### Option 2: Docker
- ✅ Docker Desktop
- ✅ 4GB RAM

### Option 3: Cloud
- ✅ Compte Railway/Heroku
- ✅ Carte bancaire (optionnel)

### Option 4: VPS
- ✅ Accès root/sudo
- ✅ Domaine configuré
- ✅ Certificat SSL

---

## 📊 COMPARAISON RAPIDE

```
┌─────────────┬───────────┬──────────┬─────────┬─────────┐
│ Critère     │ Local     │ Docker   │ Cloud   │ VPS     │
├─────────────┼───────────┼──────────┼─────────┼─────────┤
│ Temps setup │ 2-3 min   │ 5-10 min │ 10 min  │ 20 min  │
│ Coût        │ Gratuit   │ Gratuit  │ Gratuit │ 5-20$/mo│
│ Facilité    │ ⭐⭐⭐   │ ⭐⭐    │ ⭐⭐   │ ⭐     │
│ Production  │ ✗         │ ✓        │ ✓✓      │ ✓✓✓     │
│ Scalabilité │ Limitée   │ Moyenne  │ Bonne   │ Excellent│
└─────────────┴───────────┴──────────┴─────────┴─────────┘
```

---

## ✅ CHECKLIST PRE-DÉPLOIEMENT

- [ ] Toutes les variables d'env configurées
- [ ] Base de données testée
- [ ] API testée (POST /auth/token, GET /accounts/me)
- [ ] Frontend teste les routes principales
- [ ] CORS configuré correctement
- [ ] Secret key changée en production
- [ ] DEBUG = False en production
- [ ] Backup de la base configuré

---

## 🚨 PROBLÈMES COURANTS

### "Port 8000 déjà utilisé"
```bash
# Trouver le processus
lsof -i :8000

# Tuer le processus
kill -9 <PID>
```

### "Connexion à la base de données échoue"
```bash
# Vérifier PostgreSQL
psql -U postgres -h localhost

# Réinitialiser migrations
python manage.py migrate --fake-initial
```

### "CORS erreur"
- Ajouter le domaine à ALLOWED_HOSTS
- Vérifier CORS_ALLOWED_ORIGINS dans settings.py

---

## 📞 SUPPORT & RESSOURCES

- Docker: https://docs.docker.com/compose/
- Django: https://docs.djangoproject.com/en/5.2/
- React: https://react.dev/
- Railway: https://docs.railway.app/
