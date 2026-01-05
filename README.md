# Système Pédagogique Moderne

Une interface web moderne et élégante permettant au directeur de consulter et gérer tous les espaces pédagogiques avec leurs utilisateurs.

## ✨ Fonctionnalités

### Interface Moderne
- **Design moderne** : Interface avec dégradés, animations et design responsive
- **Navigation intuitive** : Barre de navigation avec accès rapide aux fonctionnalités
- **Cartes interactives** : Espaces présentés sous forme de cartes avec effets hover

### Gestion Complète
- **Tableau de bord** : Vue d'ensemble avec statistiques en temps réel
- **Utilisateurs** : Ajout, modification et suppression d'utilisateurs
- **Espaces** : Création et gestion des espaces pédagogiques
- **Rôles variés** : Support pour formateurs, étudiants, techniciens, administrateurs, secrétaires, etc.

### Base de Données
- **SQLite intégré** : Base de données locale robuste
- **Données persistantes** : Toutes les modifications sont sauvegardées
- **Structure optimisée** : Tables pour espaces et utilisateurs avec relations

## 🚀 Installation et Lancement

1. **Installer les dépendances** :
   ```bash
   pip install -r requirements.txt
   ```

2. **Lancer l'application** :
   ```bash
   python index.py
   ```

3. **Accéder à l'interface** :
   Ouvrez votre navigateur à l'adresse `http://127.0.0.1:5000/`

## 🎨 Interface Utilisateur

### Tableau de Bord
- **Statistiques visuelles** : Nombre d'espaces, utilisateurs totaux, formateurs, étudiants
- **Cartes d'espaces** : Chaque espace avec ses utilisateurs colorés par rôle
- **Actions rapides** : Boutons d'ajout/modification/suppression

### Gestion des Utilisateurs
- **Ajout intuitif** : Formulaire avec icônes et validation
- **Modification facile** : Interface d'édition avec présélection des valeurs
- **Suppression sécurisée** : Confirmations avant suppression

### Gestion des Espaces
- **Création simple** : Formulaire pour nouveaux espaces pédagogiques
- **Modification** : Édition des noms et descriptions
- **Suppression** : Avec confirmation de sécurité

## 🛠 Technologies Utilisées

- **Backend** : Flask (Python)
- **Base de données** : SQLite
- **Frontend** : Bootstrap 5, Font Awesome, Google Fonts (Poppins)
- **Styling** : CSS3 avec dégradés et animations

## 📊 Rôles Supportés

- 🎓 **Formateur** : Enseignants et formateurs
- 📚 **Étudiant** : Apprenants et élèves
- 🔧 **Technicien** : Personnel technique
- 👑 **Administrateur** : Gestion administrative
- 📝 **Secrétaire** : Personnel administratif
- ❓ **Autre** : Rôles personnalisés

## 🎯 **Fonctionnalités HTML/CSS Avancées**

### Interface Interactive
- **Animations CSS** : Transitions fluides, effets hover, animations d'entrée
- **Bouton flottant (FAB)** : Menu flottant pour actions rapides
- **Modales Bootstrap** : Fenêtres modales pour détails statistiques
- **Tooltips** : Infobulles informatives sur les boutons
- **Dropdowns natifs** : Utilisation de `<details>/<summary>` pour les statistiques

### Formulaires Dynamiques
- **Navigation par étapes** : Formulaire multi-étapes avec indicateurs visuels
- **Validation temps réel** : Compteurs de caractères, aperçus de rôles
- **Résumé interactif** : Aperçu des données saisies
- **Animations de chargement** : Indicateurs visuels lors des actions

### Effets Visuels
- **Effets de lueur** : Animations shimmer sur les cartes
- **Dégradés avancés** : Combinaisons de couleurs modernes
- **Transformations 3D** : Effets de profondeur et de perspective
- **Notifications toast** : Messages de feedback animés

### Composants HTML5
- **Éléments sémantiques** : Utilisation appropriée des balises HTML5
- **Formulaires accessibles** : Labels, placeholders, attributs ARIA
- **Médias responsives** : Images et icônes adaptatives
- **API moderne** : Utilisation des dernières fonctionnalités CSS3/HTML5

## 🎯 **Fonctionnalités Interactives**

### Tableau de Bord
- **Cartes cliquables** : Statistiques avec modales détaillées
- **Animations au scroll** : Effets d'entrée progressifs
- **Menu flottant** : Accès rapide aux actions principales
- **Barre de progression** : Indicateur de chargement visuel

### Gestion des Données
- **Confirmations améliorées** : Dialogues avec icônes et animations
- **Notifications temps réel** : Feedback visuel pour les actions
- **États de chargement** : Spinners et indicateurs de progression
- **Transitions fluides** : Animations entre les états

### Expérience Utilisateur
- **Design responsive** : Adaptation parfaite à tous les écrans
- **Accessibilité** : Contraste, focus, navigation clavier
- **Performance** : Animations optimisées, chargement progressif
- **Feedback visuel** : États hover, focus, et actifs
- ✅ Navigation intuitive
- ✅ Statistiques en temps réel

## 📁 **Structure des Fichiers**

```
consutatation/
├── index.py                 # Application Flask principale
├── pedagogical_system.db    # Base de données SQLite
├── styles.css              # Feuille de styles CSS séparée (exemple)
├── requirements.txt         # Dépendances Python
├── README.md               # Documentation
└── templates/
    ├── dashboard.html      # Page principale avec interface moderne
    ├── add_user.html       # Formulaire d'ajout d'utilisateur
    ├── add_space.html      # Formulaire d'ajout d'espace
    ├── edit_user.html      # Modification d'utilisateur
    └── edit_space.html     # Modification d'espace
```
