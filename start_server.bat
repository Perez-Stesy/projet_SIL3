@echo off
echo ========================================
echo   Demarrage du serveur Django
echo ========================================
echo.

cd backend
echo Verification des migrations...
python manage.py makemigrations
if %errorlevel% neq 0 (
    echo Erreur lors de la creation des migrations
    pause
    exit /b %errorlevel%
)
echo.
echo Application des migrations...
python manage.py migrate
if %errorlevel% neq 0 (
    echo Erreur lors de l'application des migrations
    pause
    exit /b %errorlevel%
)
echo.
echo ========================================
echo   Serveur Django demarre sur http://localhost:8000
echo   Appuyez sur Ctrl+C pour arreter
echo ========================================
echo.
python manage.py runserver

