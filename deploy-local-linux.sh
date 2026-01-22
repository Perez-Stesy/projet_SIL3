#!/bin/bash

# =========================================
# DÉPLOIEMENT LOCAL - LINUX/MAC
# Plateforme Pédagogique
# =========================================

set -e

echo ""
echo "╔════════════════════════════════════╗"
echo "║  DÉPLOIEMENT LOCAL - LINUX/MAC     ║"
echo "║  Plateforme Pédagogique            ║"
echo "╚════════════════════════════════════╝"
echo ""

# Vérifier Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Installez Python 3.10+"
    exit 1
fi

# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js n'est pas installé. Installez Node.js 18+"
    exit 1
fi

echo "✅ Python et Node.js détectés"

# ========== BACKEND ==========
echo ""
echo "[1/4] Configuration du Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Création du virtual environment..."
    python3 -m venv venv
fi

echo "Activation du virtual environment..."
source venv/bin/activate

echo "Installation des dépendances..."
pip install -q -r requirements.txt

echo "Migrations de la base de données..."
python manage.py migrate --noinput > /dev/null 2>&1

echo "✅ Backend configuré"

# ========== FRONTEND ==========
cd ../frontend
echo ""
echo "[2/4] Configuration du Frontend..."

if [ ! -d "node_modules" ]; then
    echo "Installation des dépendances npm..."
    npm install -q
fi

echo "✅ Frontend configuré"

# ========== DÉMARRAGE ==========
echo ""
echo "[3/4] Démarrage des services..."
cd ..

echo ""
echo "🚀 Démarrage du Backend (port 8000)..."
cd backend
source venv/bin/activate
python manage.py runserver 0.0.0.0:8000 &
BACKEND_PID=$!

sleep 3

echo "🚀 Démarrage du Frontend (port 5173)..."
cd ../frontend
npm run dev &
FRONTEND_PID=$!

echo ""
echo "╔════════════════════════════════════╗"
echo "║  ✅ SERVICES DÉMARRÉS              ║"
echo "╠════════════════════════════════════╣"
echo "║  Frontend: http://localhost:5173   ║"
echo "║  Backend:  http://localhost:8000   ║"
echo "║  Admin:    http://localhost:8000/admin ║"
echo "╚════════════════════════════════════╝"
echo ""
echo "Appuyez sur Ctrl+C pour arrêter les services"

# Garder les processus actifs
wait
