import psycopg2
import sys

print("Test de connexion à PostgreSQL...")
print("Veuillez entrer le mot de passe PostgreSQL si demandé.")

try:
    # Essayer avec le mot de passe du fichier .env
    from dotenv import load_dotenv
    import os
    load_dotenv()
    
    password = os.getenv('DB_PASSWORD', 'postgres')
    print(f"Tentative de connexion avec le mot de passe du fichier .env...")
    
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password=password,
        database='postgres'
    )
    print("✓ Connexion réussie!")
    conn.close()
except Exception as e:
    print(f"✗ Erreur de connexion: {e}")
    print("\nVeuillez vérifier:")
    print("1. Que PostgreSQL est démarré")
    print("2. Que le mot de passe dans backend/.env est correct")
    print("3. Que l'utilisateur 'postgres' existe")
    sys.exit(1)
