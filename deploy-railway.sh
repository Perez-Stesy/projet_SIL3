#!/bin/bash

# ============================================================
# DÉPLOIEMENT RAILWAY - SCRIPT AUTOMATISÉ
# ============================================================

set -e

echo ""
echo "╔════════════════════════════════════╗"
echo "║  DÉPLOIEMENT RAILWAY.APP           ║"
echo "║  Plateforme Pédagogique            ║"
echo "╚════════════════════════════════════╝"
echo ""

# Vérifier Git
if ! command -v git &> /dev/null; then
    echo "❌ Git n'est pas installé"
    exit 1
fi

# Vérifier Node/NPM
if ! command -v npm &> /dev/null; then
    echo "❌ npm n'est pas installé"
    exit 1
fi

echo "✅ Git et npm détectés"
echo ""

# Vérifier dépôt Git
if [ ! -d ".git" ]; then
    echo "⚠️  Pas de repository Git détecté"
    read -p "Créer un repository Git? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        git init
        git add .
        git commit -m "Initial commit - Plateforme Pédagogique"
    fi
fi

# Installer Railway CLI
echo "Vérification de Railway CLI..."
if ! command -v railway &> /dev/null; then
    echo "Installation de Railway CLI..."
    npm install -g @railway/cli
fi

echo "✅ Railway CLI prêt"
echo ""

# Menu de sélection
echo "Sélectionnez votre action:"
echo "1) Déployer nouveau projet"
echo "2) Redéployer projet existant"
echo "3) Voir logs en temps réel"
echo "4) Exécuter migrations"
echo "5) Créer superuser"
echo ""
read -p "Votre choix [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "🚀 Déploiement nouveau projet..."
        echo ""
        
        # Se connecter
        echo "Connexion à Railway..."
        railway login
        
        # Initialiser
        echo ""
        echo "Initialisation du projet..."
        railway init
        
        # Build frontend
        echo ""
        echo "[1/3] Build du frontend..."
        cd frontend
        npm install -q
        npm run build
        cd ..
        echo "✅ Frontend construit"
        
        # Pousser sur GitHub
        echo ""
        echo "[2/3] Connexion GitHub..."
        read -p "Entrez votre username GitHub: " github_user
        read -p "Entrez le nom du repository: " repo_name
        
        git remote add origin https://github.com/$github_user/$repo_name.git 2>/dev/null || true
        git branch -M main 2>/dev/null || true
        git push -u origin main
        echo "✅ Code sur GitHub"
        
        # Déployer
        echo ""
        echo "[3/3] Déploiement..."
        railway up
        
        echo ""
        echo "✅ Déploiement réussi!"
        echo ""
        echo "Prochaines étapes:"
        echo "1. Ajouter PostgreSQL: railway service add postgresql"
        echo "2. Voir les logs: railway logs -f"
        echo "3. Exécuter migrations: railway run python manage.py migrate"
        echo "4. URL: railway status"
        ;;
        
    2)
        echo ""
        echo "🔄 Redéploiement..."
        railway redeploy
        
        echo ""
        echo "✅ Redéploiement lancé!"
        echo "Voir les logs: railway logs -f"
        ;;
        
    3)
        echo ""
        echo "📊 Logs en temps réel..."
        echo "Appuyez sur Ctrl+C pour arrêter"
        railway logs -f
        ;;
        
    4)
        echo ""
        echo "🗄️  Exécution des migrations..."
        railway run python manage.py migrate
        
        echo "✅ Migrations exécutées!"
        ;;
        
    5)
        echo ""
        echo "👤 Création d'un superuser..."
        railway run python manage.py createsuperuser
        
        echo "✅ Superuser créé!"
        ;;
        
    *)
        echo "❌ Choix invalide"
        exit 1
        ;;
esac

echo ""
