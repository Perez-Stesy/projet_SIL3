@echo off
REM =========================================
REM DÉPLOIEMENT LOCAL - WINDOWS
REM Plateforme Pédagogique
REM =========================================

setlocal enabledelayedexpansion
echo.
echo ╔════════════════════════════════════╗
echo ║  DÉPLOIEMENT LOCAL - WINDOWS       ║
echo ║  Plateforme Pédagogique            ║
echo ╚════════════════════════════════════╝
echo.

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé. Installez Python 3.10+
    pause
    exit /b 1
)

REM Vérifier Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js n'est pas installé. Installez Node.js 18+
    pause
    exit /b 1
)

echo ✅ Python et Node.js détectés

REM ========== BACKEND ==========
echo.
echo [1/4] Configuration du Backend...
cd backend

if not exist venv (
    echo Création du virtual environment...
    python -m venv venv
)

echo Activation du virtual environment...
call venv\Scripts\activate.bat

echo Installation des dépendances...
pip install -q -r requirements.txt 2>nul

echo Migrations de la base de données...
python manage.py migrate --noinput >nul 2>&1

echo ✅ Backend configuré

REM ========== FRONTEND ==========
cd ..\frontend
echo.
echo [2/4] Configuration du Frontend...

if not exist node_modules (
    echo Installation des dépendances npm...
    call npm install -q 2>nul
)

echo ✅ Frontend configuré

REM ========== DÉMARRAGE ==========
echo.
echo [3/4] Démarrage des services...
cd ..

echo.
echo 🚀 Démarrage du Backend (port 8000)...
start "Backend" cmd /k "cd backend && venv\Scripts\activate.bat && python manage.py runserver 0.0.0.0:8000"

timeout /t 3 /nobreak >nul

echo 🚀 Démarrage du Frontend (port 5173)...
start "Frontend" cmd /k "cd frontend && npm run dev"

echo.
echo ╔════════════════════════════════════╗
echo ║  ✅ SERVICES DÉMARRÉS              ║
echo ╠════════════════════════════════════╣
echo ║  Frontend: http://localhost:5173   ║
echo ║  Backend:  http://localhost:8000   ║
echo ║  Admin:    http://localhost:8000/admin ║
echo ╚════════════════════════════════════╝
echo.
echo Appuyez sur Ctrl+C pour arrêter les services
pause

cd ..
