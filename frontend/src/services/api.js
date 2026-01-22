import axios from 'axios'

// Utiliser la variable d'environnement ou une valeur par défaut
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000/api'

const api = axios.create({
  baseURL: API_BASE_URL,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      localStorage.removeItem('token')
      window.location.href = '/connexion'
    }
    return Promise.reject(error)
  },
)

export async function connexion(email, motDePasse) {
  const response = await api.post('/auth/token/', {
    email,
    password: motDePasse,
  })
  const { access } = response.data
  localStorage.setItem('token', access)
  return access
}

export async function recupererProfilConnecte() {
  const response = await api.get('/accounts/me/')
  return response.data
}

export async function creerCompteUtilisateur({ email, role, nom, prenom, sexe }) {
  const response = await api.post('/accounts/users/', {
    email,
    first_name: prenom,
    last_name: nom,
    sexe,
    role,
  })
  return response.data
}

export async function activerCompte({ email, motDePasse, confirmation }) {
  const response = await api.post('/accounts/activate/', {
    email,
    password: motDePasse,
    password_confirmation: confirmation,
  })
  return response.data
}

// Promotions
export async function listerPromotions() {
  const response = await api.get('/academics/promotions/')
  return response.data
}

export async function creerPromotion({ nom, annee }) {
  const response = await api.post('/academics/promotions/', {
    name: nom,
    year: annee,
  })
  return response.data
}

// Matières
export async function listerMatieres() {
  const response = await api.get('/academics/subjects/')
  return response.data
}

export async function creerMatiere({ code, nom }) {
  const response = await api.post('/academics/subjects/', {
    code,
    name: nom,
  })
  return response.data
}

// Étudiants / promotions
export async function affecterEtudiantPromotion({ idUtilisateurEtudiant, idPromotion }) {
  const response = await api.post('/academics/students/assign/', {
    student_user_id: Number(idUtilisateurEtudiant),
    promotion_id: Number(idPromotion),
  })
  return response.data
}

// Espaces pédagogiques
export async function listerEspaces() {
  const response = await api.get('/pedagogy/spaces/')
  return response.data
}

export async function listerMesEspacesFormateur() {
  const response = await api.get('/pedagogy/spaces/me/formateur/')
  return response.data
}

export async function listerMesEspacesEtudiant() {
  const response = await api.get('/pedagogy/spaces/me/etudiant/')
  return response.data
}

// Utilisateurs (Directeur)
export async function listerUtilisateurs({ role } = {}) {
  const params = {}
  if (role) params.role = role
  const response = await api.get('/accounts/users/list/', { params })
  return response.data
}

// Profils étudiants (Directeur)
export async function listerProfilsEtudiants() {
  const response = await api.get('/academics/students/')
  return response.data
}

// Travaux / assignations / livraisons / évaluations
export async function creerTravail({ idEspace, type, titre, consignes, dateLimite }) {
  const response = await api.post('/works/works/', {
    space: Number(idEspace),
    type,
    title: titre,
    instructions: consignes,
    due_at: dateLimite || null,
  })
  return response.data
}

export async function assignerTravailIndividuel({ idTravail, idProfilEtudiant }) {
  const response = await api.post('/works/assignments/', {
    work: Number(idTravail),
    student: Number(idProfilEtudiant),
  })
  return response.data
}

export async function listerMesTravauxAssignes() {
  const response = await api.get('/works/me/assignments/')
  return response.data
}

export async function livrerTravail({ idAssignation, fichier }) {
  const formData = new FormData()
  formData.append('assignment_id', String(idAssignation))
  formData.append('file', fichier)
  const response = await api.post('/works/submissions/', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return response.data
}

export async function evaluerLivraison({ idLivraison, note, noteMax, commentaire, publier }) {
  const response = await api.post('/works/evaluations/', {
    submission_id: Number(idLivraison),
    grade: note,
    max_grade: noteMax,
    comment: commentaire || '',
    published: Boolean(publier),
  })
  return response.data
}

export async function listerLivraisonsAevaluer() {
  const response = await api.get('/works/me/submissions/formateur/')
  return response.data
}

export async function listerMesEvaluations() {
  const response = await api.get('/works/me/evaluations/')
  return response.data
}

export async function consulterClassement({ idPromotion, annee }) {
  const response = await api.get('/works/ranking/', {
    params: { promotion_id: Number(idPromotion), year: Number(annee) },
  })
  return response.data
}

export async function creerEspace({ idMatiere, annee, idPromotion }) {
  const response = await api.post('/pedagogy/spaces/', {
    subject: Number(idMatiere),
    year: Number(annee),
    promotion: Number(idPromotion),
  })
  return response.data
}

export async function affecterFormateurEspace({ idEspace, idUtilisateurFormateur }) {
  const response = await api.post(`/pedagogy/spaces/${idEspace}/assign-trainer/`, {
    trainer_user_id: Number(idUtilisateurFormateur),
  })
  return response.data
}

export async function ajouterEtudiantEspace({ idEspace, idProfilEtudiant }) {
  const response = await api.post(`/pedagogy/spaces/${idEspace}/add-student/`, {
    student_profile_id: Number(idProfilEtudiant),
  })
  return response.data
}

export { api }

