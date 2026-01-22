@echo off
echo ========================================
echo   Plateforme Pedagogique
echo   Demarrage Backend + Frontend
echo ========================================
echo.

REM Créer deux fenêtres séparées pour le backend et le frontend
echo [INFO] Demarrage du backend dans une nouvelle fenetre...
start "Backend - Plateforme Pedagogique" cmd /k "cd backend && start.bat"

timeout /t 3 /nobreak >nul

echo [INFO] Demarrage du frontend dans une nouvelle fenetre...
start "Frontend - Plateforme Pedagogique" cmd /k "cd frontend && start.bat"

echo.
echo ========================================
echo   Les deux services sont en cours de demarrage...
echo.
echo   Backend:  http://127.0.0.1:8000
echo   Frontend: http://localhost:5173
echo ========================================
echo.
echo Appuyez sur une touche pour fermer cette fenetre...
echo (Les fenetres du backend et frontend resteront ouvertes)
pause >nul
