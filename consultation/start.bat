@echo off
echo ========================================
echo   Application de Consultation des Travaux
echo ========================================
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Python n'est pas installe ou n'est pas dans le PATH.
    echo.
    echo Veuillez installer Python depuis https://www.python.org/downloads/
    echo Assurez-vous de cocher "Add Python to PATH" lors de l'installation.
    pause
    exit /b 1
)

echo [OK] Python detecte
python --version
echo.

REM Vérifier si les dépendances sont installées
echo Verification des dependances...
python -c "import django" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installation de Django...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo [ERREUR] Echec de l'installation des dependances.
        pause
        exit /b 1
    )
)

echo [OK] Dependances installees
echo.

REM Créer les migrations si nécessaire
if not exist "db.sqlite3" (
    echo [INFO] Creation des migrations...
    python manage.py makemigrations
    if errorlevel 1 (
        echo [ERREUR] Echec de la creation des migrations.
        pause
        exit /b 1
    )
    
    echo [INFO] Application des migrations...
    python manage.py migrate
    if errorlevel 1 (
        echo [ERREUR] Echec de l'application des migrations.
        pause
        exit /b 1
    )
    
    echo [INFO] Creation de donnees d'exemple...
    python manage.py create_sample_data
)

echo.
echo ========================================
echo   Demarrage du serveur Django
echo ========================================
echo.
echo L'application sera accessible sur: http://127.0.0.1:8000/
echo Appuyez sur Ctrl+C pour arreter le serveur
echo.

python manage.py runserver

pause


