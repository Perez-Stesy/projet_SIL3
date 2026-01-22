# 🔧 Corrections apportées et guide de déploiement

## ✅ Problèmes corrigés

### 1. Problème d'authentification

**Problème identifié :**
- Le backend d'authentification personnalisé (`EmailBackend`) n'était pas configuré dans les settings Django
- Le serializer JWT avait une vérification stricte qui pouvait bloquer certaines connexions

**Corrections apportées :**
- ✅ Ajout de `AUTHENTICATION_BACKENDS` dans `backend/backend/settings.py`
- ✅ Amélioration du serializer JWT pour une meilleure gestion des erreurs
- ✅ Normalisation de l'email (insensible à la casse) lors de l'authentification

### 2. Configuration pour la production

**Améliorations :**
- ✅ Configuration des variables d'environnement pour SECRET_KEY, DEBUG, ALLOWED_HOSTS
- ✅ Configuration CORS adaptative (dev/production)
- ✅ Configuration STATIC_ROOT pour la collecte des fichiers statiques

### 3. Fichiers de déploiement créés

- ✅ `backend/Dockerfile` - Image Docker pour le backend Django
- ✅ `frontend/Dockerfile` - Image Docker pour le frontend React
- ✅ `frontend/nginx.conf` - Configuration Nginx pour servir le frontend
- ✅ `docker-compose.yml` - Orchestration complète de l'application
- ✅ `backend/gunicorn_config.py` - Configuration Gunicorn pour la production
- ✅ `backend/.env.example` - Template de variables d'environnement
- ✅ `DEPLOY.md` - Guide complet de déploiement
- ✅ `start.sh` - Script de démarrage automatisé

## 🚀 Démarrage rapide

### Option 1 : Avec Docker (Recommandé)

```bash
# 1. Configurer les variables d'environnement
cp backend/.env.example backend/.env
# Éditer backend/.env avec vos valeurs

# 2. Démarrer l'application
chmod +x start.sh
./start.sh

# OU manuellement:
docker-compose up -d
docker-compose exec backend python manage.py migrate
docker-compose exec backend python manage.py createsuperuser
```

### Option 2 : Sans Docker

Voir le fichier `DEPLOY.md` pour les instructions détaillées.

## 🔍 Vérification du problème de connexion

Pour tester si le problème de connexion est résolu :

1. **Vérifier que le backend est démarré :**
   ```bash
   docker-compose ps
   # ou
   curl http://localhost:8000/api/accounts/me/
   ```

2. **Vérifier les logs en cas d'erreur :**
   ```bash
   docker-compose logs backend
   ```

3. **Tester la connexion :**
   - Assurez-vous que le compte utilisateur a été activé (mot de passe défini)
   - Utilisez l'email exact (insensible à la casse maintenant)
   - Vérifiez que le compte est actif (`is_active=True`)

## 📝 Notes importantes

1. **Première connexion :** Les comptes créés par le Directeur doivent être activés via la page d'activation avant de pouvoir se connecter.

2. **Superutilisateur :** Pour créer un compte Directeur, utilisez :
   ```bash
   docker-compose exec backend python manage.py createsuperuser
   ```

3. **Variables d'environnement critiques :**
   - `SECRET_KEY` : Doit être changé en production
   - `DEBUG` : Doit être `False` en production
   - `ALLOWED_HOSTS` : Doit inclure votre domaine en production
   - `CORS_ALLOWED_ORIGINS` : Doit inclure l'URL de votre frontend en production

## 🌐 Déploiement en production

1. **Préparer le serveur :**
   - Installer Docker et Docker Compose
   - Configurer un nom de domaine
   - Obtenir un certificat SSL (Let's Encrypt)

2. **Configurer l'application :**
   ```bash
   # Sur le serveur
   git clone <votre-repo>
   cd plateforme-pedagogique
   cp backend/.env.example backend/.env
   # Éditer backend/.env avec les valeurs de production
   ```

3. **Lancer l'application :**
   ```bash
   ./start.sh
   ```

4. **Configurer Nginx (optionnel mais recommandé) :**
   - Voir `DEPLOY.md` pour la configuration complète
   - Configurer SSL avec Let's Encrypt

## 🐛 Dépannage

### Erreur de connexion persistante

1. Vérifier que le compte a un mot de passe utilisable :
   ```bash
   docker-compose exec backend python manage.py shell
   >>> from accounts.models import User
   >>> user = User.objects.get(email='votre@email.com')
   >>> user.has_usable_password()  # Doit retourner True
   ```

2. Vérifier que le compte est actif :
   ```bash
   >>> user.is_active  # Doit retourner True
   ```

3. Réinitialiser le mot de passe si nécessaire :
   ```bash
   >>> user.set_password('nouveau_mot_de_passe')
   >>> user.save()
   ```

### Erreur CORS

- Vérifier que `CORS_ALLOWED_ORIGINS` dans `.env` inclut l'URL de votre frontend
- En développement, `CORS_ALLOW_ALL_ORIGINS=True` est activé automatiquement

### Erreur de base de données

- Vérifier que PostgreSQL est démarré : `docker-compose ps db`
- Vérifier les variables d'environnement de la base de données dans `.env`
- Vérifier les logs : `docker-compose logs db`

## 📞 Support

Pour plus d'informations, consultez :
- `DEPLOY.md` - Guide complet de déploiement
- Les logs des services : `docker-compose logs -f`
