# Guide de la Base de Données

## Base de Données Actuelle

Le projet utilise **SQLite** par défaut, qui est une base de données légère et parfaite pour le développement.

### Fichier de base de données
- **Emplacement**: `db.sqlite3` (à la racine du projet)
- **Type**: SQLite3
- **Avantages**: 
  - Pas besoin de serveur séparé
  - Facile à utiliser
  - Parfait pour le développement et les petits projets

## Initialiser des Données de Test

Pour remplir la base de données avec des données de test :

```bash
cd backend
python manage.py init_data
```

Cette commande créera :
- 3 formateurs de test
- 3 espaces pédagogiques de test
- Des assignations de formateurs aux espaces

## Visualiser la Base de Données

### Option 1: Interface d'administration Django

1. Créez un superutilisateur :
```bash
python manage.py createsuperuser
```

2. Démarrez le serveur :
```bash
python manage.py runserver
```

3. Accédez à : `http://localhost:8000/admin/`

### Option 2: Outils SQLite

Vous pouvez utiliser des outils comme :
- **DB Browser for SQLite** : https://sqlitebrowser.org/
- **SQLiteStudio** : https://sqlitestudio.pl/
- **VS Code Extension** : SQLite Viewer

Ouvrez simplement le fichier `db.sqlite3` avec l'un de ces outils.

## Migrer vers PostgreSQL (Optionnel)

Si vous souhaitez utiliser PostgreSQL pour la production :

### 1. Installer PostgreSQL

Téléchargez depuis : https://www.postgresql.org/download/

### 2. Installer le driver Python

```bash
pip install psycopg2-binary
```

Ou utilisez le fichier :
```bash
pip install -r requirements_postgresql.txt
```

### 3. Créer la base de données PostgreSQL

```sql
CREATE DATABASE projet_sil3;
CREATE USER votre_utilisateur WITH PASSWORD 'votre_mot_de_passe';
GRANT ALL PRIVILEGES ON DATABASE projet_sil3 TO votre_utilisateur;
```

### 4. Modifier settings.py

Remplacez la section `DATABASES` dans `backend/settings.py` :

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'projet_sil3',
        'USER': 'votre_utilisateur',
        'PASSWORD': 'votre_mot_de_passe',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 5. Appliquer les migrations

```bash
python manage.py migrate
```

## Structure de la Base de Données

### Table: `espaces_pedagogiques_formateur`
- `id` (Primary Key)
- `nom` (CharField)
- `prenom` (CharField)
- `email` (EmailField, unique)
- `telephone` (CharField, nullable)
- `date_creation` (DateTimeField)

### Table: `espaces_pedagogiques_espacepedagogique`
- `id` (Primary Key)
- `matiere` (CharField)
- `code` (CharField, unique)
- `description` (TextField, nullable)
- `date_creation` (DateTimeField)

### Table: `espaces_pedagogiques_espacepedagogique_formateurs`
- Table de liaison Many-to-Many entre EspacePedagogique et Formateur
- `espacepedagogique_id` (Foreign Key)
- `formateur_id` (Foreign Key)

## Commandes Utiles

### Voir les migrations appliquées
```bash
python manage.py showmigrations
```

### Créer de nouvelles migrations
```bash
python manage.py makemigrations
```

### Appliquer les migrations
```bash
python manage.py migrate
```

### Accéder au shell Django
```bash
python manage.py shell
```

Exemple d'utilisation dans le shell :
```python
from espaces_pedagogiques.models import EspacePedagogique, Formateur

# Lister tous les espaces
espaces = EspacePedagogique.objects.all()
for espace in espaces:
    print(f"{espace.matiere} - {espace.code}")

# Lister tous les formateurs
formateurs = Formateur.objects.all()
for formateur in formateurs:
    print(f"{formateur.prenom} {formateur.nom} - {formateur.email}")
```

## Sauvegarde et Restauration

### Sauvegarder la base SQLite
Copiez simplement le fichier `db.sqlite3` vers un autre emplacement.

### Restaurer
Remplacez `db.sqlite3` par votre sauvegarde.

## Notes Importantes

⚠️ **Ne commitez JAMAIS** le fichier `db.sqlite3` dans Git si il contient des données sensibles. Le fichier est déjà dans `.gitignore`.

✅ Pour le développement, SQLite est parfait et suffisant.

✅ Pour la production, considérez PostgreSQL ou MySQL.

