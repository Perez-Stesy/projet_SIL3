# Guide de déploiement - Plateforme Pédagogique

Ce guide explique comment déployer l'application sur un serveur en ligne.

## Prérequis

- Docker et Docker Compose installés
- Un serveur avec au moins 2GB de RAM
- Un nom de domaine (optionnel mais recommandé)

## Option 1 : Déploiement avec Docker Compose (Recommandé)

### 1. Préparer l'environnement

```bash
# Cloner le projet sur le serveur
git clone <votre-repo> plateforme-pedagogique
cd plateforme-pedagogique
```

### 2. Configurer les variables d'environnement

```bash
# Copier le fichier d'exemple
cp backend/.env.example backend/.env

# Éditer le fichier .env avec vos valeurs
nano backend/.env
```

Variables importantes à configurer :
- `SECRET_KEY` : Générez une clé secrète Django (utilisez `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
- `DEBUG=False` : En production, toujours mettre à False
- `ALLOWED_HOSTS` : Ajoutez votre nom de domaine (ex: `votredomaine.com,www.votredomaine.com`)
- `CORS_ALLOWED_ORIGINS` : URL de votre frontend (ex: `https://votredomaine.com`)
- `DB_PASSWORD` : Mot de passe fort pour PostgreSQL

### 3. Lancer l'application

```bash
# Construire et démarrer les conteneurs
docker-compose up -d

# Vérifier les logs
docker-compose logs -f

# Créer un superutilisateur (Directeur)
docker-compose exec backend python manage.py createsuperuser
```

### 4. Collecter les fichiers statiques

```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

## Option 2 : Déploiement manuel (sans Docker)

### Backend (Django)

1. **Installer les dépendances**

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
pip install gunicorn
```

2. **Configurer la base de données**

```bash
# Créer la base de données PostgreSQL
createdb plateforme_pedagogique

# Appliquer les migrations
python manage.py migrate

# Créer un superutilisateur
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic --noinput
```

3. **Lancer avec Gunicorn**

```bash
gunicorn --bind 0.0.0.0:8000 --workers 3 backend.wsgi:application
```

### Frontend (React)

1. **Installer les dépendances et construire**

```bash
cd frontend
npm install
npm run build
```

2. **Servir avec Nginx**

Copiez le contenu du dossier `dist` vers `/var/www/html` ou configurez Nginx pour pointer vers ce dossier.

## Configuration Nginx (Recommandé pour production)

Créez un fichier `/etc/nginx/sites-available/plateforme` :

```nginx
# Redirection HTTP vers HTTPS
server {
    listen 80;
    server_name votredomaine.com www.votredomaine.com;
    return 301 https://$server_name$request_uri;
}

# Configuration HTTPS
server {
    listen 443 ssl http2;
    server_name votredomaine.com www.votredomaine.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    # Frontend
    location / {
        root /var/www/plateforme-frontend;
        try_files $uri $uri/ /index.html;
    }

    # Backend API
    location /api/ {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Media files
    location /media/ {
        alias /path/to/backend/media/;
    }

    # Static files
    location /static/ {
        alias /path/to/backend/staticfiles/;
    }
}
```

Activez la configuration :
```bash
sudo ln -s /etc/nginx/sites-available/plateforme /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

## Configuration SSL avec Let's Encrypt

```bash
# Installer Certbot
sudo apt-get install certbot python3-certbot-nginx

# Obtenir un certificat
sudo certbot --nginx -d votredomaine.com -d www.votredomaine.com
```

## Maintenance

### Mettre à jour l'application

```bash
# Avec Docker
git pull
docker-compose build
docker-compose up -d
docker-compose exec backend python manage.py migrate

# Sans Docker
git pull
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
sudo systemctl restart gunicorn
```

### Sauvegarder la base de données

```bash
# Avec Docker
docker-compose exec db pg_dump -U postgres plateforme_pedagogique > backup.sql

# Sans Docker
pg_dump -U postgres plateforme_pedagogique > backup.sql
```

### Restaurer la base de données

```bash
# Avec Docker
docker-compose exec -T db psql -U postgres plateforme_pedagogique < backup.sql

# Sans Docker
psql -U postgres plateforme_pedagogique < backup.sql
```

## Dépannage

### Vérifier les logs

```bash
# Docker
docker-compose logs -f backend
docker-compose logs -f frontend

# Gunicorn
sudo journalctl -u gunicorn -f
```

### Tester la connexion à la base de données

```bash
docker-compose exec backend python manage.py dbshell
```

### Vérifier les permissions

```bash
# S'assurer que les fichiers statiques sont accessibles
sudo chown -R www-data:www-data /path/to/staticfiles
sudo chown -R www-data:www-data /path/to/media
```

## Sécurité

1. **Changez la SECRET_KEY** en production
2. **Mettez DEBUG=False** en production
3. **Configurez ALLOWED_HOSTS** avec votre domaine
4. **Utilisez HTTPS** avec Let's Encrypt
5. **Configurez un firewall** (UFW sur Ubuntu)
6. **Mettez à jour régulièrement** les dépendances
7. **Sauvegardez régulièrement** la base de données

## Support

En cas de problème, vérifiez :
- Les logs des services
- La configuration des variables d'environnement
- La connectivité réseau
- Les permissions des fichiers
