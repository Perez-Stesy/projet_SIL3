# Documentation API - Gestion des Espaces Pédagogiques

## Base URL
```
http://localhost:8000/api
```

## Endpoints

### 1. Créer un Espace Pédagogique (Epic 1)

**POST** `/espaces/creer/`

Créer un nouvel espace pédagogique vide pour une matière.

**Body:**
```json
{
    "matiere": "Génie Logiciel",
    "code": "GL-SIL3",
    "description": "Description optionnelle"
}
```

**Réponse succès (201):**
```json
{
    "success": true,
    "message": "Espace pédagogique créé avec succès",
    "data": {
        "id": 1,
        "matiere": "Génie Logiciel",
        "code": "GL-SIL3",
        "description": "Description optionnelle",
        "date_creation": "2025-12-18T17:00:00Z",
        "formateurs": [],
        "nombre_formateurs": 0
    }
}
```

**Réponse erreur (400):**
```json
{
    "success": false,
    "message": "Erreur lors de la création de l'espace pédagogique",
    "errors": {
        "code": ["Un espace pédagogique avec ce code existe déjà."]
    }
}
```

---

### 2. Lister tous les Espaces Pédagogiques

**GET** `/espaces/`

**Réponse succès (200):**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "matiere": "Génie Logiciel",
            "code": "GL-SIL3",
            "description": "...",
            "date_creation": "2025-12-18T17:00:00Z",
            "formateurs": [],
            "nombre_formateurs": 0
        }
    ]
}
```

---

### 3. Détails d'un Espace Pédagogique

**GET** `/espaces/<id>/`

**Réponse succès (200):**
```json
{
    "success": true,
    "data": {
        "id": 1,
        "matiere": "Génie Logiciel",
        "code": "GL-SIL3",
        "description": "...",
        "date_creation": "2025-12-18T17:00:00Z",
        "formateurs": [
            {
                "id": 1,
                "nom": "Dupont",
                "prenom": "Jean",
                "email": "jean.dupont@example.com",
                "telephone": "+33 6 12 34 56 78",
                "date_creation": "2025-12-18T17:00:00Z"
            }
        ],
        "nombre_formateurs": 1
    }
}
```

---

### 4. Ajouter un Formateur à un Espace (Epic 2)

**POST** `/espaces/<espace_id>/ajouter-formateur/`

Insérer un formateur dans un espace pédagogique.

**Body:**
```json
{
    "formateur_id": 1
}
```

**Réponse succès (200):**
```json
{
    "success": true,
    "message": "Formateur ajouté avec succès à l'espace pédagogique",
    "data": {
        "id": 1,
        "matiere": "Génie Logiciel",
        "code": "GL-SIL3",
        "formateurs": [...],
        "nombre_formateurs": 1
    }
}
```

**Réponse erreur (400):**
```json
{
    "success": false,
    "message": "Ce formateur est déjà assigné à cet espace pédagogique"
}
```

---

### 5. Créer un Formateur

**POST** `/formateurs/creer/`

**Body:**
```json
{
    "nom": "Dupont",
    "prenom": "Jean",
    "email": "jean.dupont@example.com",
    "telephone": "+33 6 12 34 56 78"
}
```

**Réponse succès (201):**
```json
{
    "success": true,
    "message": "Formateur créé avec succès",
    "data": {
        "id": 1,
        "nom": "Dupont",
        "prenom": "Jean",
        "email": "jean.dupont@example.com",
        "telephone": "+33 6 12 34 56 78",
        "date_creation": "2025-12-18T17:00:00Z"
    }
}
```

---

### 6. Lister tous les Formateurs

**GET** `/formateurs/`

**Réponse succès (200):**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "nom": "Dupont",
            "prenom": "Jean",
            "email": "jean.dupont@example.com",
            "telephone": "+33 6 12 34 56 78",
            "date_creation": "2025-12-18T17:00:00Z"
        }
    ]
}
```

---

## Codes de statut HTTP

- `200 OK` - Requête réussie
- `201 Created` - Ressource créée avec succès
- `400 Bad Request` - Erreur de validation
- `404 Not Found` - Ressource non trouvée
- `500 Internal Server Error` - Erreur serveur

## Exemples d'utilisation avec cURL

### Créer un espace pédagogique
```bash
curl -X POST http://localhost:8000/api/espaces/creer/ \
  -H "Content-Type: application/json" \
  -d '{"matiere": "Génie Logiciel", "code": "GL-SIL3"}'
```

### Créer un formateur
```bash
curl -X POST http://localhost:8000/api/formateurs/creer/ \
  -H "Content-Type: application/json" \
  -d '{"nom": "Dupont", "prenom": "Jean", "email": "jean@example.com"}'
```

### Ajouter un formateur à un espace
```bash
curl -X POST http://localhost:8000/api/espaces/1/ajouter-formateur/ \
  -H "Content-Type: application/json" \
  -d '{"formateur_id": 1}'
```

