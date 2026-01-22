# 🔥 COMMANDES ESSENTIELLES DE DÉPLOIEMENT

## ⚡ DÉPLOIEMENT EN UNE LIGNE

### Option 1: Local (Windows)
```bash
deploy-local-windows.bat
```

### Option 2: Local (Linux/Mac)
```bash
chmod +x deploy-local-linux.sh && ./deploy-local-linux.sh
```

### Option 3: Docker
```bash
chmod +x deploy-docker.sh && ./deploy-docker.sh
```

### Option 4: Railway
```bash
npm install -g @railway/cli && railway login && railway up
```

---

## 📋 COMMANDES PAR CAS D'USAGE

### Vérifier le système
```bash
python --version          # Doit être 3.10+
node --version            # Doit être 18+
docker --version          # Pour Docker
```

### Installation dépendances
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
npm install
```

### Migrations base de données
```bash
cd backend
python manage.py migrate
python manage.py createsuperuser  # Compte admin
```

### Démarrer les services

#### Local dev (deux terminaux)
```bash
# Terminal 1 - Backend
cd backend
python manage.py runserver 0.0.0.0:8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

#### Docker
```bash
# Développement
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d

# Voir logs
docker-compose logs -f

# Arrêter
docker-compose down
```

### Accéder aux services
```bash
Frontend:  http://localhost:5173  (local dev)
           http://localhost:3000  (Docker dev)
           http://localhost       (Docker prod)

Backend:   http://localhost:8000

Admin:     http://localhost:8000/admin
```

### Build pour production
```bash
# Frontend
cd frontend
npm run build     # Crée dist/

# Backend
cd backend
python manage.py collectstatic --noinput
```

### Debugging

#### Voir erreurs frontend
```bash
# Console du navigateur
F12 → Console tab
```

#### Voir erreurs backend
```bash
# Logs Django
python manage.py runserver --verbosity=2

# Logs Docker
docker-compose logs -f backend
```

#### Tester API
```bash
# Ping API
curl http://localhost:8000/api/accounts/me/

# Authentification
curl -X POST http://localhost:8000/api/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com", "password":"password123"}'
```

### Gestion de la base de données

#### Accéder PostgreSQL
```bash
# Depuis host
psql -h localhost -U postgres -d plateforme_pedagogique

# Depuis Docker
docker-compose exec db psql -U postgres -d plateforme_pedagogique
```

#### Réinitialiser migrations
```bash
cd backend
python manage.py migrate --fake-initial
```

#### Créer migration
```bash
python manage.py makemigrations [app_name]
```

### Problèmes courants

#### Port déjà utilisé
```bash
# Trouver le processus
lsof -i :8000  # Port 8000
lsof -i :5173  # Port 5173

# Tuer le processus
kill -9 <PID>

# Ou changer le port
python manage.py runserver 8001
```

#### Permissions fichiers
```bash
chmod +x deploy-*.sh      # Scripts exécutables
chmod 755 static/         # Dossiers
```

#### Réinstaller dépendances
```bash
# Backend
rm -rf backend/venv
python -m venv backend/venv
source backend/venv/bin/activate
pip install -r requirements.txt

# Frontend
rm -rf frontend/node_modules package-lock.json
npm install
```

### Production checklist

```bash
# 1. Vérifier config
python verify-deployment.py

# 2. Compiler frontend
npm run build

# 3. Collecter static files
python manage.py collectstatic --noinput

# 4. Migrations
python manage.py migrate

# 5. Build Docker
docker build -t plateforme:latest .

# 6. Déployer
docker-compose -f docker-compose.prod.yml up -d

# 7. Vérifier santé
curl http://localhost:8000/api/accounts/me/
```

### Monitoring & Maintenance

```bash
# Voir ressources utilisées
docker stats

# Voir tous les containers
docker ps -a

# Voir images
docker images

# Nettoyage (attention!)
docker system prune  # Supprime ressources inutilisées

# Backups
docker-compose exec db pg_dump -U postgres db_name > backup.sql

# Restore backup
docker-compose exec -T db psql -U postgres db_name < backup.sql
```

### SSH sur serveur VPS

```bash
# Connexion
ssh root@votre_ip

# Télécharger le projet
git clone votre_repo

# Déployer
docker-compose -f docker-compose.prod.yml up -d

# Logs
docker-compose logs -f

# Redémarrer
docker-compose restart
```

### Variables d'environnement

```bash
# Backend (.env)
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1,votre-domaine.com
DB_NAME=plateforme_prod
DB_USER=postgres
DB_PASSWORD=secure_password
DB_HOST=db
DB_PORT=5432

# Frontend (.env) - si nécessaire
REACT_APP_API_URL=http://localhost:8000
REACT_APP_ENV=development
```

### Déploiement CI/CD (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy
on: [push]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: docker/build-push-action@v2
      - name: Deploy to server
        run: |
          ssh user@server 'cd /app && git pull && docker-compose up -d'
```

---

## 🎯 RÉSUMÉ DES COMMANDES ESSENTIELLES

| Action | Commande |
|--------|----------|
| **Démarrer local** | `deploy-local-windows.bat` ou `deploy-local-linux.sh` |
| **Démarrer Docker** | `docker-compose up -d` |
| **Voir logs** | `docker-compose logs -f` |
| **Arrêter** | `docker-compose down` |
| **Créer admin** | `python manage.py createsuperuser` |
| **Migrations** | `python manage.py migrate` |
| **Build frontend** | `npm run build` |
| **Tester API** | `curl http://localhost:8000/api/accounts/me/` |
| **Rebuild tout** | `docker-compose down && docker-compose build --no-cache && docker-compose up -d` |

---

## ⚡ QUICK COMMAND REFERENCE

```bash
# Une seule commande pour tout
docker-compose up -d && sleep 3 && echo "✅ Services lancés!"

# Réinitialiser complètement
docker-compose down -v && docker-compose up -d

# Voir tout
docker ps -a && docker logs -f plateforme_backend
```

Bon déploiement! 🚀
