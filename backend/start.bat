@echo off
echo ========================================
echo   Plateforme Pedagogique - Backend
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Python 3.11 ou superieur
    pause
    exit /b 1
)

REM Activer l'environnement virtuel s'il existe
if exist ..\venv\Scripts\activate.bat (
    echo [INFO] Activation de l'environnement virtuel...
    call ..\venv\Scripts\activate.bat
)

REM Vérifier si le fichier .env existe, sinon créer depuis .env.example
if not exist .env (
    echo [ATTENTION] Le fichier .env n'existe pas!
    if exist .env.example (
        echo [INFO] Creation du fichier .env depuis .env.example...
        copy .env.example .env
        echo [ATTENTION] Veuillez modifier le fichier .env avec vos valeurs!
        echo Appuyez sur une touche pour continuer...
        pause >nul
    ) else (
        echo [ERREUR] Le fichier .env.example n'existe pas!
        pause
        exit /b 1
    )
)

echo [1/4] Installation des dependances...
pip install -r ..\requirements.txt
if errorlevel 1 (
    echo [ERREUR] Echec de l'installation des dependances
    pause
    exit /b 1
)

echo.
echo [2/4] Application des migrations...
python manage.py migrate
if errorlevel 1 (
    echo [ERREUR] Echec des migrations
    pause
    exit /b 1
)

echo.
echo [3/4] Collecte des fichiers statiques...
python manage.py collectstatic --noinput

echo.
echo [4/4] Demarrage du serveur Django...
echo.
echo ========================================
echo   Backend disponible sur: http://127.0.0.1:8000
echo   API disponible sur: http://127.0.0.1:8000/api
echo ========================================
echo.
python manage.py runserver
