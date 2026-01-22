# 🚂 DÉPLOIEMENT RAILWAY - 5 ÉTAPES SIMPLES

## ⏱️ Temps total: 10 minutes

---

## ÉTAPE 1: S'INSCRIRE (2 min)

Allez sur: **https://railway.app**

Cliquez "Sign up with GitHub"

✅ Compte créé!

---

## ÉTAPE 2: POUSSER LE CODE SUR GITHUB (3 min)

### Option A: Si vous avez déjà un repo GitHub
```bash
cd c:\Users\HP\Pictures\cursor2
git push origin main
```

### Option B: Si vous n'en avez pas
```bash
# 1. Créer un repo: https://github.com/new
#    Nom: plateforme-pedagogique

# 2. Pousser le code:
cd c:\Users\HP\Pictures\cursor2

git remote add origin https://github.com/VOTRE_USERNAME/plateforme-pedagogique.git
git branch -M main
git push -u origin main
```

✅ Code sur GitHub!

---

## ÉTAPE 3: CRÉER UN PROJET RAILWAY (2 min)

### Via interface web (Plus simple):
1. Allez sur: https://railway.app/dashboard
2. Cliquez **"New Project"**
3. Sélectionnez **"Deploy from GitHub"**
4. Autorisez Railway
5. Sélectionnez votre repo: **plateforme-pedagogique**
6. Sélectionnez branche: **main**
7. Attendez que Railway crée l'infrastructure

✅ Projet créé!

---

## ÉTAPE 4: AJOUTER LA BASE DE DONNÉES (2 min)

Dans le dashboard Railway:

1. Cliquez **"Add Service"**
2. Cherchez **"PostgreSQL"**
3. Cliquez **"Deploy"**

✅ Base de données liée automatiquement!

---

## ÉTAPE 5: CONFIGURER & LANCER (2 min)

### Configuration automatique:
Railway configure automatiquement les variables. Vérifiez juste:

1. Service **backend** → **Variables**
2. Ajouter:
```env
DEBUG=False
SECRET_KEY=change-this-in-production
ALLOWED_HOSTS=*.railway.app,localhost
```

### Lancer les migrations:
```bash
npm install -g @railway/cli
railway login
railway run python manage.py migrate
railway run python manage.py createsuperuser
```

✅ App déployée!

---

## 🌐 ACCÉDER À VOTRE APP

Dans le dashboard Railway:
1. Cliquez sur **"backend"**
2. Allez dans **"Deployments"**
3. Trouvez le lien public

**URL:** `https://plateforme-pedagogique-production.up.railway.app`

Ouvrez cette URL dans votre navigateur! ✨

---

## ✅ VÉRIFICATIONS

```
✓ Frontend charge: https://votre-app.railway.app
✓ API répond: https://votre-app.railway.app/api/accounts/me/
✓ Admin accessible: https://votre-app.railway.app/admin/
✓ Authentification fonctionne
```

---

## 📊 VOS LOGS EN TEMPS RÉEL

```bash
railway logs -f
```

---

## 🎉 TERMINÉ!

Votre app est maintenant en ligne sur Railway! 🚀

### Améliorations possibles:
- [ ] Configurer domaine custom
- [ ] Ajouter monitoring
- [ ] Configurer backups
- [ ] Ajouter email notifications

**Consultez RAILWAY_DEPLOYMENT.md pour plus de détails!**
