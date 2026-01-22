@echo off
echo ========================================
echo   Plateforme Pedagogique - Frontend
echo ========================================
echo.

REM Vérifier si Node.js est installé
node --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] Node.js n'est pas installe ou n'est pas dans le PATH
    echo Veuillez installer Node.js 18 ou superieur depuis https://nodejs.org
    pause
    exit /b 1
)

REM Vérifier si npm est installé
npm --version >nul 2>&1
if errorlevel 1 (
    echo [ERREUR] npm n'est pas installe
    pause
    exit /b 1
)

echo [1/2] Installation des dependances...
if not exist node_modules (
    echo Installation des packages npm (cela peut prendre quelques minutes)...
    call npm install
    if errorlevel 1 (
        echo [ERREUR] Echec de l'installation des dependances npm
        pause
        exit /b 1
    )
) else (
    echo Les dependances sont deja installees.
)

echo.
echo [2/2] Demarrage du serveur de developpement...
echo.
echo ========================================
echo   Frontend disponible sur: http://localhost:5173
echo ========================================
echo.
call npm run dev
