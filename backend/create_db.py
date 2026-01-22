import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os
from dotenv import load_dotenv

load_dotenv()

# Connexion à PostgreSQL (base de données par défaut)
conn = psycopg2.connect(
    host=os.getenv('DB_HOST', 'localhost'),
    port=os.getenv('DB_PORT', '5432'),
    user=os.getenv('DB_USER', 'postgres'),
    password=os.getenv('DB_PASSWORD', 'postgres'),
    database='postgres'  # On se connecte à la base par défaut
)

conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cur = conn.cursor()

# Vérifier si la base existe
db_name = os.getenv('DB_NAME', 'plateforme_pedagogique')
cur.execute("SELECT 1 FROM pg_database WHERE datname = %s", (db_name,))
exists = cur.fetchone()

if not exists:
    cur.execute(f'CREATE DATABASE {db_name}')
    print(f'Base de données "{db_name}" créée avec succès!')
else:
    print(f'Base de données "{db_name}" existe déjà.')

cur.close()
conn.close()
