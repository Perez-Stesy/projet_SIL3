#!/usr/bin/env python3
"""
Script de vérification pré-déploiement
Teste que tout est prêt pour la production
"""

import os
import sys
import subprocess
from pathlib import Path

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def print_header(text):
    print(f"\n{Colors.BLUE}{'='*50}{Colors.END}")
    print(f"{Colors.BLUE}{text:^50}{Colors.END}")
    print(f"{Colors.BLUE}{'='*50}{Colors.END}\n")

def check(condition, message):
    if condition:
        print(f"{Colors.GREEN}✓{Colors.END} {message}")
        return True
    else:
        print(f"{Colors.RED}✗{Colors.END} {message}")
        return False

def main():
    print_header("🔍 VÉRIFICATION PRÉ-DÉPLOIEMENT")
    
    all_ok = True
    
    # Vérifier Python
    print("Vérification du système...")
    try:
        version = subprocess.check_output(['python3', '--version']).decode().strip()
        all_ok &= check(True, f"Python installé: {version}")
    except:
        all_ok &= check(False, "Python 3 non trouvé")
    
    # Vérifier Node.js
    try:
        version = subprocess.check_output(['node', '--version']).decode().strip()
        all_ok &= check(True, f"Node.js installé: {version}")
    except:
        all_ok &= check(False, "Node.js non trouvé")
    
    # Vérifier Docker
    try:
        subprocess.check_output(['docker', '--version'])
        all_ok &= check(True, "Docker installé")
    except:
        all_ok &= check(False, "Docker non trouvé (optionnel)")
    
    # Vérifier fichiers essentiels
    print("\nVérification des fichiers...")
    backend_path = Path("backend")
    frontend_path = Path("frontend")
    
    all_ok &= check(backend_path.exists(), "Dossier backend trouvé")
    all_ok &= check(frontend_path.exists(), "Dossier frontend trouvé")
    all_ok &= check((backend_path / "requirements.txt").exists(), "requirements.txt trouvé")
    all_ok &= check((frontend_path / "package.json").exists(), "package.json trouvé")
    all_ok &= check((backend_path / ".env").exists(), "backend/.env trouvé")
    
    # Vérifier configuration
    print("\nVérification de la configuration...")
    with open(backend_path / ".env") as f:
        env_content = f.read()
        all_ok &= check("SECRET_KEY" in env_content, "SECRET_KEY configurée")
        all_ok &= check("DB_NAME" in env_content, "DB_NAME configurée")
    
    # Résumé
    print_header("📋 RÉSUMÉ")
    
    if all_ok:
        print(f"{Colors.GREEN}✓ TOUT EST PRÊT POUR LE DÉPLOIEMENT!{Colors.END}\n")
        print("Options de déploiement:")
        print(f"  1. {Colors.YELLOW}Local:{Colors.END} ./deploy-local-windows.bat")
        print(f"  2. {Colors.YELLOW}Docker:{Colors.END} ./deploy-docker.sh")
        print(f"  3. {Colors.YELLOW}Railway:{Colors.END} railway up")
        print(f"  4. {Colors.YELLOW}Guide complet:{Colors.END} Voir GUIDE_DEPLOYMENT.md")
        return 0
    else:
        print(f"{Colors.RED}✗ CERTAINES VÉRIFICATIONS ONT ÉCHOUÉ{Colors.END}\n")
        print("Veuillez corriger les problèmes avant de déployer.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
