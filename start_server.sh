#!/bin/bash

echo "========================================"
echo "  Démarrage du serveur Django"
echo "========================================"
echo ""

cd backend || exit 1

echo "Vérification des migrations..."
python manage.py makemigrations || exit 1

echo ""
echo "Application des migrations..."
python manage.py migrate || exit 1

echo ""
echo "========================================"
echo "  Serveur Django démarre sur http://localhost:8000"
echo "  Appuyez sur Ctrl+C pour arrêter"
echo "========================================"
echo ""

python manage.py runserver

