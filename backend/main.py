espaces = []

espace1 = EspacePedagogique(1, "Génie Logiciel", "GL-SIL3")

if creer_espace(espaces, espace1):
    print("✅ Espace pédagogique créé")
else:
    print("❌ Cet espace existe déjà")

from models import EspacePedagogique
from services import lister_espaces

espaces = []

espaces.append(EspacePedagogique(1, "Génie Logiciel", "GL-SIL3"))
espaces.append(EspacePedagogique(2, "Base de Données", "BD-SIL3"))

liste = lister_espaces(espaces)

for espace in liste:
    print(f"{espace.id} - {espace.matiere} ({espace.code})")
