import { useEffect, useState } from 'react'
import {
  consulterClassement,
  listerMesEvaluations,
  listerMesTravauxAssignes,
  livrerTravail,
  recupererProfilConnecte,
} from '../services/api'
import { FaFileAlt, FaUpload, FaChartBar, FaTrophy, FaSignOutAlt } from 'react-icons/fa'
import './TableauDeBordEtudiant.css'

function TableauDeBordEtudiant() {
  const [ongletActif, setOngletActif] = useState('travaux')
  const [profil, setProfil] = useState(null)
  const [assignations, setAssignations] = useState([])
  const [evaluations, setEvaluations] = useState([])
  const [message, setMessage] = useState('')
  const [erreur, setErreur] = useState('')
  const [enCours, setEnCours] = useState(false)

  // Livraison
  const [idAssignation, setIdAssignation] = useState('')
  const [fichier, setFichier] = useState(null)

  // Classement
  const [idPromotionClassement, setIdPromotionClassement] = useState('')
  const [anneeClassement, setAnneeClassement] = useState(new Date().getFullYear())
  const [classement, setClassement] = useState(null)

  useEffect(() => {
    async function charger() {
      try {
        const [profilCourant, mesTravaux, mesEvaluations] = await Promise.all([
          recupererProfilConnecte(),
          listerMesTravauxAssignes(),
          listerMesEvaluations(),
        ])
        setProfil(profilCourant)
        setAssignations(mesTravaux)
        setEvaluations(mesEvaluations)
      } catch (e) {
        console.error(e)
        setErreur("Impossible de charger vos données.")
      }
    }
    charger()
  }, [])

  async function handleLivrer(e) {
    e.preventDefault()
    setMessage('')
    setErreur('')
    setEnCours(true)
    try {
      if (!fichier) {
        setErreur("Veuillez choisir un fichier.")
        return
      }
      await livrerTravail({ idAssignation, fichier })
      setMessage("Livraison effectuée avec succès.")
      setIdAssignation('')
      setFichier(null)
    } catch (err) {
      console.error(err)
      setErreur("Erreur lors de la livraison.")
    } finally {
      setEnCours(false)
    }
  }

  async function handleClassement(e) {
    e.preventDefault()
    setMessage('')
    setErreur('')
    setEnCours(true)
    try {
      const data = await consulterClassement({
        idPromotion: idPromotionClassement,
        annee: anneeClassement,
      })
      setClassement(data)
      setMessage('Classement chargé.')
    } catch (err) {
      console.error(err)
      setErreur("Erreur lors du chargement du classement.")
    } finally {
      setEnCours(false)
    }
  }

  return (
    <div className="page-etudiant">
      <aside className="sidebar">
        <div className="sidebar-entete">
          <h2>Étudiant</h2>
          {profil && (
            <p className="sidebar-bienvenue">
              Bienvenue,{' '}
              <strong>
                {profil.first_name} {profil.last_name}
              </strong>
            </p>
          )}
        </div>
        <nav className="sidebar-nav">
          <button
            className={`nav-bouton ${ongletActif === 'travaux' ? 'actif' : ''}`}
            onClick={() => setOngletActif('travaux')}
          >
            <FaFileAlt /> Mes Travaux
          </button>
          <button
            className={`nav-bouton ${ongletActif === 'evaluations' ? 'actif' : ''}`}
            onClick={() => setOngletActif('evaluations')}
          >
            <FaChartBar /> Mes Évaluations
          </button>
          <button
            className={`nav-bouton ${ongletActif === 'classement' ? 'actif' : ''}`}
            onClick={() => setOngletActif('classement')}
          >
            <FaTrophy /> Classement
          </button>
        </nav>
        <button
          type="button"
          className="btn-deconnexion"
          onClick={() => {
            localStorage.removeItem('token')
            window.location.href = '/connexion'
          }}
        >
          <FaSignOutAlt /> Déconnexion
        </button>
      </aside>

      <main className="contenu-directeur">
        <header className="entete">
          <div>
            <h1>Espace Étudiant</h1>
            <p className="sous-titre-directeur">
              Consulter mes travaux, livrer, voir mes évaluations et le classement.
            </p>
          </div>
        </header>

        {message && <div className="alerte alerte-succes">{message}</div>}
        {erreur && <div className="alerte alerte-erreur">{erreur}</div>}

        <section className="carte-directeur">
          <h2><FaFileAlt /> Mes travaux assignés</h2>
          {assignations.length === 0 ? (
            <p>Aucun travail assigné pour le moment.</p>
          ) : (
            <ul>
              {assignations.map((a) => (
                <li key={a.id}>
                  <strong>{a.work_title}</strong> — assignation #{a.id}
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="carte-directeur">
          <h2><FaUpload /> Livrer un travail</h2>
          <form onSubmit={handleLivrer} className="formulaire">
            <label>
              Id assignation
              <input value={idAssignation} onChange={(e) => setIdAssignation(e.target.value)} required />
            </label>
            <label>
              Fichier
              <input type="file" onChange={(e) => setFichier(e.target.files?.[0] || null)} required />
            </label>
            <button disabled={enCours}>Livrer</button>
          </form>
        </section>

        <section className="carte-directeur">
          <h2><FaChartBar /> Mes évaluations publiées</h2>
          {evaluations.length === 0 ? (
            <p>Aucune évaluation publiée pour le moment.</p>
          ) : (
            <ul>
              {evaluations.map((ev) => (
                <li key={ev.id}>
                  Note: {ev.grade}/{ev.max_grade} — {ev.comment || 'Sans commentaire'}
                </li>
              ))}
            </ul>
          )}
        </section>

        <section className="carte-directeur">
          <h2><FaTrophy /> Classement</h2>
          <form onSubmit={handleClassement} className="formulaire">
            <label>
              Id promotion
              <input
                value={idPromotionClassement}
                onChange={(e) => setIdPromotionClassement(e.target.value)}
                required
              />
            </label>
            <label>
              Année
              <input
                type="number"
                value={anneeClassement}
                onChange={(e) => setAnneeClassement(e.target.value)}
                required
              />
            </label>
            <button disabled={enCours}>Consulter</button>
          </form>

          {classement?.results?.length ? (
            <div className="liste-simple" style={{ marginTop: '1rem' }}>
              <h3>
                {classement.promotion.name} ({classement.promotion.year})
              </h3>
              <ol>
                {classement.results.map((r) => (
                  <li key={`${r.student_profile_id}-${r.rank}`}>
                    {r.email} — moyenne: {r.average}
                  </li>
                ))}
              </ol>
            </div>
          ) : null}
        </section>
      </main>
    </div>
  )
}

export default TableauDeBordEtudiant

