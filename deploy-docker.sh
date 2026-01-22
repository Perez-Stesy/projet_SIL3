#!/bin/bash

# =========================================
# DÉPLOIEMENT DOCKER COMPOSE
# Plateforme Pédagogique
# =========================================

set -e

echo ""
echo "╔════════════════════════════════════╗"
echo "║  DÉPLOIEMENT DOCKER COMPOSE        ║"
echo "║  Plateforme Pédagogique            ║"
echo "╚════════════════════════════════════╝"
echo ""

# Vérifier Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé"
    echo "Installez Docker: https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé"
    echo "Installez Docker Compose: https://docs.docker.com/compose/install/"
    exit 1
fi

echo "✅ Docker et Docker Compose détectés"
echo ""

# Menu de sélection
echo "Sélectionnez le mode de déploiement:"
echo "1) Développement (développement.yml)"
echo "2) Production (docker-compose.prod.yml)"
echo "3) Arrêter tous les services"
echo ""
read -p "Votre choix [1-3]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Déploiement en DÉVELOPPEMENT..."
        echo ""
        
        echo "[1/3] Construction des images..."
        docker-compose build
        
        echo "[2/3] Démarrage des services..."
        docker-compose up -d
        
        echo "[3/3] Attente du démarrage..."
        sleep 5
        
        echo ""
        echo "╔════════════════════════════════════╗"
        echo "║  ✅ SERVICES DÉMARRÉS (DEV)        ║"
        echo "╠════════════════════════════════════╣"
        echo "║  Frontend: http://localhost:3000   ║"
        echo "║  Backend:  http://localhost:8000   ║"
        echo "║  DB:       localhost:5432          ║"
        echo "╚════════════════════════════════════╝"
        echo ""
        echo "Voir les logs: docker-compose logs -f"
        echo "Arrêter:      docker-compose down"
        ;;
        
    2)
        echo ""
        echo "🚀 Déploiement en PRODUCTION..."
        echo ""
        
        # Créer .env.prod si inexistant
        if [ ! -f "backend/.env.prod" ]; then
            echo "⚠️  backend/.env.prod n'existe pas"
            echo "Création d'un fichier template..."
            cp backend/.env backend/.env.prod
            echo "✅ Fichier créé. MODIFIEZ-LE AVANT DE CONTINUER!"
            echo "Éditez: backend/.env.prod"
            exit 1
        fi
        
        echo "[1/3] Construction des images..."
        docker-compose -f docker-compose.prod.yml build
        
        echo "[2/3] Démarrage des services..."
        docker-compose -f docker-compose.prod.yml up -d
        
        echo "[3/3] Attente du démarrage..."
        sleep 5
        
        echo ""
        echo "╔════════════════════════════════════╗"
        echo "║  ✅ SERVICES DÉMARRÉS (PROD)       ║"
        echo "╠════════════════════════════════════╣"
        echo "║  Frontend: http://localhost        ║"
        echo "║  Backend:  http://localhost:8000   ║"
        echo "║  DB:       localhost:5432 (local)  ║"
        echo "╚════════════════════════════════════╝"
        echo ""
        echo "Voir les logs: docker-compose -f docker-compose.prod.yml logs -f"
        echo "Arrêter:      docker-compose -f docker-compose.prod.yml down"
        ;;
        
    3)
        echo ""
        echo "🛑 Arrêt des services..."
        docker-compose down
        docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
        echo "✅ Services arrêtés"
        ;;
        
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
