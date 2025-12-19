def creer_espace(espace_list, nouvel_espace):
    for espace in espace_list:
        if espace.code == nouvel_espace.code:
            return False
    espace_list.append(nouvel_espace)
    return True

from backend.models import EspacePedagogique
def ajouter_formateur(espace, formateur):
    if formateur not in espace.formateurs:
        espace.formateurs.append(formateur)
        return True
    return False
    def lister_membres(espace):
    return {
        "formateurs": espace.formateurs,
        "etudiants": espace.etudiants
    }

def ajouter_etudiant(espace, etudiant):
    if etudiant not in espace.etudiants:
        espace.etudiants.append(etudiant)
        return True
    return False
def supprimer_espace(espace_list, code_espace):
    for espace in espace_list:
        if espace.code == code_espace:
            espace_list.remove(espace)
            return True
    return False
def trouver_espace(espace_list, code_espace):
    for espace in espace_list:
        if espace.code == code_espace:
            return espace
    return None

    def lister_espaces(espaces):
    return espaces
