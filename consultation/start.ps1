Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Application de Consultation des Travaux" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Vérifier si Python est installé
try {
    $pythonVersion = python --version 2>&1
    Write-Host "[OK] Python detecte: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "[ERREUR] Python n'est pas installe ou n'est pas dans le PATH." -ForegroundColor Red
    Write-Host ""
    Write-Host "Veuillez installer Python depuis https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Assurez-vous de cocher 'Add Python to PATH' lors de l'installation." -ForegroundColor Yellow
    Read-Host "Appuyez sur Entree pour quitter"
    exit 1
}

Write-Host ""

# Vérifier si les dépendances sont installées
Write-Host "Verification des dependances..." -ForegroundColor Yellow
try {
    python -c "import django" 2>$null
    Write-Host "[OK] Dependances installees" -ForegroundColor Green
} catch {
    Write-Host "[INFO] Installation de Django..." -ForegroundColor Yellow
    pip install -r requirements.txt
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERREUR] Echec de l'installation des dependances." -ForegroundColor Red
        Read-Host "Appuyez sur Entree pour quitter"
        exit 1
    }
}

Write-Host ""

# Créer les migrations si nécessaire
if (-not (Test-Path "db.sqlite3")) {
    Write-Host "[INFO] Creation des migrations..." -ForegroundColor Yellow
    python manage.py makemigrations
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERREUR] Echec de la creation des migrations." -ForegroundColor Red
        Read-Host "Appuyez sur Entree pour quitter"
        exit 1
    }
    
    Write-Host "[INFO] Application des migrations..." -ForegroundColor Yellow
    python manage.py migrate
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERREUR] Echec de l'application des migrations." -ForegroundColor Red
        Read-Host "Appuyez sur Entree pour quitter"
        exit 1
    }
    
    Write-Host "[INFO] Creation de donnees d'exemple..." -ForegroundColor Yellow
    python manage.py create_sample_data
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Demarrage du serveur Django" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "L'application sera accessible sur: http://127.0.0.1:8000/" -ForegroundColor Green
Write-Host "Appuyez sur Ctrl+C pour arreter le serveur" -ForegroundColor Yellow
Write-Host ""

python manage.py runserver


