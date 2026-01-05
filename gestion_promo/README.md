# 🎓 Gestion des Promotions - Application Django Moderne

Une application web moderne et élégante pour gérer les promotions académiques, avec un backend Django et un front-end HTML/CSS/JavaScript de qualité professionnelle.

## ✨ Fonctionnalités

- **Création de promotions** : Interface intuitive avec formulaire moderne
- **Gestion des années** : Association d'une promotion à une année académique
- **Visualisation élégante** : Cartes animées avec informations détaillées
- **Filtrage** : Filtrez par promotions actives/inactives
- **Design moderne** : Interface avec animations fluides et effets visuels
- **Responsive** : Compatible mobile, tablette et desktop
- **API REST** : Backend Django avec endpoints JSON

## 🚀 Installation et Démarrage

### Prérequis

- Python 3.8+
- pip
- Virtual environment (recommandé)

### Étapes d'installation

1. **Activer l'environnement virtuel** (déjà créé dans le projet)
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

2. **Installer Django** (déjà installé si vous avez suivi les étapes)
   ```bash
   pip install django
   ```

3. **Appliquer les migrations** (déjà fait)
   ```bash
   python manage.py migrate
   ```

4. **Créer un superutilisateur** (optionnel, pour l'admin Django)
   ```bash
   python manage.py createsuperuser
   ```

5. **Lancer le serveur de développement**
   ```bash
   python manage.py runserver
   ```

6. **Accéder à l'application**
   - Interface principale : http://127.0.0.1:8000/
   - Admin Django : http://127.0.0.1:8000/admin/

## 📁 Structure du Projet

```
gestion_promo/
├── gestion_promo/          # Configuration du projet Django
│   ├── settings.py         # Paramètres du projet
│   ├── urls.py            # URLs principales
│   └── ...
├── promotions/             # Application principale
│   ├── models.py          # Modèle Promotion
│   ├── views.py           # Vues et API
│   ├── urls.py            # URLs de l'application
│   ├── admin.py           # Configuration admin Django
│   └── templates/         # Templates HTML
│       └── promotions/
│           └── index.html  # Page principale
├── static/                 # Fichiers statiques
│   ├── css/
│   │   └── style.css      # Styles CSS modernes
│   └── js/
│       └── app.js         # JavaScript pour l'interactivité
├── manage.py              # Script de gestion Django
└── db.sqlite3             # Base de données SQLite
```

## 🎨 Caractéristiques du Design

### Interface Moderne
- **Animations fluides** : Transitions et effets visuels élégants
- **Glassmorphism** : Effets de verre dépoli pour les cartes
- **Gradients animés** : Arrière-plan avec orbes animés
- **Micro-interactions** : Retours visuels sur chaque action

### Couleurs et Thème
- Palette de couleurs moderne avec gradients
- Mode sombre/clair adaptatif
- Couleurs personnalisables par promotion

### Responsive Design
- Adapté à tous les écrans
- Navigation tactile optimisée
- Grille flexible pour les cartes

## 🔧 Utilisation

### Créer une Promotion

1. Cliquez sur le bouton **+** (FAB) en bas à droite
2. Remplissez le formulaire :
   - **Nom** : Nom de la promotion (ex: "Master Informatique 2024-2025")
   - **Année** : Année académique
   - **Dates** : Date de début et de fin
   - **Description** : Description optionnelle
   - **Nombre d'étudiants** : Nombre d'étudiants dans la promotion
   - **Couleur** : Couleur personnalisée pour la carte
   - **Statut** : Active/Inactive
3. Cliquez sur **Créer la Promotion**

### Filtrer les Promotions

Utilisez les boutons de filtre en haut de la section :
- **Toutes** : Affiche toutes les promotions
- **Actives** : Affiche uniquement les promotions actives
- **Inactives** : Affiche uniquement les promotions inactives

### Supprimer une Promotion

Cliquez sur le bouton **🗑️ Supprimer** sur la carte de la promotion.

## 🛠️ API Endpoints

L'application expose une API REST simple :

- `GET /api/promotions/` : Liste toutes les promotions
- `POST /api/promotions/create/` : Crée une nouvelle promotion
- `DELETE /api/promotions/<id>/delete/` : Supprime une promotion

### Exemple de requête POST

```json
{
  "nom": "Master Informatique 2024-2025",
  "annee": 2024,
  "description": "Promotion de master en informatique",
  "date_debut": "2024-09-01",
  "date_fin": "2025-06-30",
  "nombre_etudiants": 45,
  "active": true,
  "couleur": "#6366f1"
}
```

## 📝 Modèle de Données

### Promotion

- `nom` : Nom de la promotion (CharField, max 200)
- `annee` : Année académique (IntegerField, 2000-2100)
- `description` : Description détaillée (TextField, optionnel)
- `date_debut` : Date de début (DateField)
- `date_fin` : Date de fin (DateField)
- `nombre_etudiants` : Nombre d'étudiants (PositiveIntegerField)
- `active` : Statut actif/inactif (BooleanField)
- `couleur` : Couleur hexadécimale (CharField, max 7)
- `date_creation` : Date de création (DateTimeField, auto)
- `date_modification` : Date de modification (DateTimeField, auto)

### Propriétés calculées

- `duree_jours` : Durée en jours entre début et fin
- `est_en_cours` : Vérifie si la promotion est actuellement en cours

## 🎯 Raccourcis Clavier

- `Ctrl/Cmd + N` : Ouvrir le formulaire de création
- `Escape` : Fermer le modal

## 🐛 Dépannage

### Erreur de migration
```bash
python manage.py makemigrations
python manage.py migrate
```

### Erreur de fichiers statiques
Vérifiez que `STATICFILES_DIRS` est bien configuré dans `settings.py`

### Erreur CSRF
Les vues API utilisent `@csrf_exempt` pour simplifier les appels. En production, utilisez des tokens CSRF appropriés.

## 📄 Licence

Ce projet est un exemple éducatif. Libre d'utilisation et de modification.

## 👨‍💻 Développement

Pour contribuer ou modifier l'application :

1. Modifiez les modèles dans `promotions/models.py`
2. Créez les migrations : `python manage.py makemigrations`
3. Appliquez les migrations : `python manage.py migrate`
4. Modifiez les vues dans `promotions/views.py`
5. Personnalisez le CSS dans `static/css/style.css`
6. Ajoutez des fonctionnalités JS dans `static/js/app.js`

---

**Profitez de cette application moderne pour gérer vos promotions académiques ! 🎓✨**

