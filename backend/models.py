class EspacePedagogique:
    def __init__(self, id, matiere, code):
        self.id = id
        self.matiere = matiere
        self.code = code
        self.formateurs = []
        self.etudiants = []
