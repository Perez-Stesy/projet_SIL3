# Guide de Configuration PostgreSQL

Ce guide vous explique comment configurer PostgreSQL pour remplacer SQLite dans votre application Django.

## Prérequis

1. **Installer PostgreSQL** sur votre système :
   - Windows : Téléchargez depuis [postgresql.org](https://www.postgresql.org/download/windows/)
   - Ou utilisez un gestionnaire de paquets comme Chocolatey : `choco install postgresql`

2. **Installer le driver Python** pour PostgreSQL :
   ```bash
   pip install psycopg2-binary
   ```

## Configuration

### 1. Créer la base de données PostgreSQL

Connectez-vous à PostgreSQL (via pgAdmin ou en ligne de commande) :

```sql
-- Se connecter en tant que superutilisateur postgres
-- Créer la base de données
CREATE DATABASE plateforme_pedagogique;

-- Créer un utilisateur (optionnel, vous pouvez utiliser postgres)
CREATE USER plateforme_user WITH PASSWORD 'votre_mot_de_passe';

-- Donner les permissions
GRANT ALL PRIVILEGES ON DATABASE plateforme_pedagogique TO plateforme_user;
```

### 2. Créer le fichier .env

Créez un fichier `.env` dans le dossier `backend/` avec le contenu suivant :

```env
# Configuration PostgreSQL
USE_POSTGRESQL=true
DB_NAME=plateforme_pedagogique
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe
DB_HOST=localhost
DB_PORT=5432
```

**⚠️ Important :** Remplacez `votre_mot_de_passe` par le mot de passe que vous avez défini pour PostgreSQL.

### 3. Vérifier la configuration

Le fichier `backend/backend/settings.py` est déjà configuré pour :
- Essayer de se connecter à PostgreSQL en premier
- Utiliser SQLite en fallback si PostgreSQL n'est pas disponible

### 4. Appliquer les migrations

Une fois PostgreSQL configuré, appliquez les migrations :

```bash
cd backend
python manage.py migrate
```

### 5. Créer un superutilisateur (Directeur)

```bash
python manage.py createsuperuser
```

Entrez :
- Email : l'email du directeur
- Username : un nom d'utilisateur
- Password : un mot de passe

**Note :** Selon le modèle User, si vous créez un superutilisateur, il sera automatiquement défini comme DIRECTEUR.

## Utiliser SQLite (par défaut)

Si vous préférez utiliser SQLite (plus simple pour le développement), créez un fichier `.env` avec :

```env
USE_POSTGRESQL=false
```

Ou supprimez simplement le fichier `.env` - SQLite sera utilisé par défaut.

## Vérification

Pour vérifier quelle base de données est utilisée, lancez le serveur Django :

```bash
cd backend
python manage.py runserver
```

Si PostgreSQL est configuré correctement, vous ne verrez pas de message d'erreur. Si PostgreSQL n'est pas disponible, vous verrez :
```
PostgreSQL non disponible, utilisation de SQLite
```

## Dépannage

### Erreur : "psycopg2 not found"
```bash
pip install psycopg2-binary
```

### Erreur : "password authentication failed"
- Vérifiez le mot de passe dans le fichier `.env`
- Vérifiez que l'utilisateur PostgreSQL existe

### Erreur : "database does not exist"
- Créez la base de données avec la commande SQL ci-dessus
- Vérifiez le nom de la base dans le fichier `.env`

### Erreur : "connection refused"
- Vérifiez que PostgreSQL est démarré
- Vérifiez le port (par défaut 5432)
- Vérifiez l'hôte (localhost)

## Commandes utiles PostgreSQL

```bash
# Se connecter à PostgreSQL
psql -U postgres

# Lister les bases de données
\l

# Se connecter à une base de données
\c plateforme_pedagogique

# Lister les tables
\dt

# Quitter
\q
```
