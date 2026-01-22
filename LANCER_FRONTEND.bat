@echo off
echo ========================================
echo   LANCEMENT MANUEL DU FRONTEND
echo ========================================
echo.
echo Ces commandes seront executees:
echo   1. cd frontend
echo   2. Installation des dependances (si necessaire)
echo   3. Demarrage du serveur de developpement
echo.
echo Appuyez sur une touche pour continuer...
pause >nul

cd frontend

REM Installer les dependances si node_modules n'existe pas
if not exist node_modules (
    echo [INFO] Installation des dependances npm...
    npm install
) else (
    echo [INFO] Les dependances sont deja installees
)

REM Demarrer le serveur
echo.
echo ========================================
echo   Frontend demarre sur http://localhost:5173
echo ========================================
echo.
npm run dev

pause
