# Configuration PostgreSQL

## Installation de PostgreSQL

### Windows
1. Téléchargez PostgreSQL depuis https://www.postgresql.org/download/windows/
2. Installez PostgreSQL avec les paramètres par défaut
3. Notez le mot de passe du superutilisateur `postgres` que vous définissez lors de l'installation

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
```

### macOS
```bash
brew install postgresql
brew services start postgresql
```

## Création de la base de données

1. Connectez-vous à PostgreSQL :
```bash
psql -U postgres
```

2. Créez la base de données :
```sql
CREATE DATABASE plateforme_pedagogique;
```

3. Créez un utilisateur (optionnel, vous pouvez utiliser `postgres`) :
```sql
CREATE USER votre_utilisateur WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE plateforme_pedagogique TO votre_utilisateur;
```

4. Quittez psql :
```sql
\q
```

## Configuration du fichier .env

Créez un fichier `.env` dans le répertoire `backend/` avec le contenu suivant :

```env
DB_NAME=plateforme_pedagogique
DB_USER=postgres
DB_PASSWORD=votre_mot_de_passe_postgres
DB_HOST=localhost
DB_PORT=5432
```

## Installation des dépendances Python

```bash
cd backend
pip install -r ../requirements.txt
```

## Migration de la base de données

```bash
python manage.py makemigrations
python manage.py migrate
```

## Création d'un superutilisateur (si nécessaire)

```bash
python manage.py createsuperuser
```

## Lancement du serveur

```bash
python manage.py runserver
```
