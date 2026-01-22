@echo off
echo ========================================
echo   LANCEMENT MANUEL DU BACKEND
echo ========================================
echo.
echo Ces commandes seront executees:
echo   1. cd backend
echo   2. Activation de l'environnement virtuel
echo   3. Installation des dependances
echo   4. Migrations
echo   5. Demarrage du serveur
echo.
echo Appuyez sur une touche pour continuer...
pause >nul

cd backend

REM Activer l'environnement virtuel
if exist ..\venv\Scripts\activate.bat (
    echo [INFO] Activation de l'environnement virtuel...
    call ..\venv\Scripts\activate.bat
) else (
    echo [ATTENTION] Environnement virtuel non trouve, utilisation de Python global
)

REM Installer les dependances
echo [INFO] Installation des dependances...
pip install -r ..\requirements.txt

REM Migrations
echo [INFO] Application des migrations...
python manage.py migrate

REM Demarrer le serveur
echo.
echo ========================================
echo   Backend demarre sur http://127.0.0.1:8000
echo ========================================
echo.
python manage.py runserver

pause
