#!/bin/bash

# Script de démarrage pour la plateforme pédagogique

echo "🚀 Démarrage de la plateforme pédagogique..."

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Vérifier si le fichier .env existe
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Le fichier backend/.env n'existe pas."
    echo "📝 Création du fichier .env à partir de .env.example..."
    if [ -f "backend/.env.example" ]; then
        cp backend/.env.example backend/.env
        echo "✅ Fichier .env créé. Veuillez le modifier avec vos valeurs avant de continuer."
        echo "⚠️  IMPORTANT: Modifiez SECRET_KEY, DEBUG, et ALLOWED_HOSTS dans backend/.env"
        exit 1
    else
        echo "❌ Le fichier backend/.env.example n'existe pas."
        exit 1
    fi
fi

# Construire et démarrer les conteneurs
echo "🔨 Construction des images Docker..."
docker-compose build

echo "🚀 Démarrage des services..."
docker-compose up -d

# Attendre que la base de données soit prête
echo "⏳ Attente de la base de données..."
sleep 5

# Appliquer les migrations
echo "📦 Application des migrations..."
docker-compose exec -T backend python manage.py migrate

# Collecter les fichiers statiques
echo "📁 Collecte des fichiers statiques..."
docker-compose exec -T backend python manage.py collectstatic --noinput

echo "✅ Application démarrée avec succès!"
echo ""
echo "📋 Informations:"
echo "   - Frontend: http://localhost"
echo "   - Backend API: http://localhost:8000/api"
echo "   - Admin Django: http://localhost:8000/admin"
echo ""
echo "📝 Pour créer un superutilisateur (Directeur):"
echo "   docker-compose exec backend python manage.py createsuperuser"
echo ""
echo "📊 Pour voir les logs:"
echo "   docker-compose logs -f"
echo ""
echo "🛑 Pour arrêter l'application:"
echo "   docker-compose down"
