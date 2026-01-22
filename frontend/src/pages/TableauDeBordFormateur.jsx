import { useEffect, useMemo, useState } from 'react'
import {
  assignerTravailIndividuel,
  consulterClassement,
  creerTravail,
  evaluerLivraison,
  listerMesEspacesFormateur,
  listerLivraisonsAevaluer,
  recupererProfilConnecte,
} from '../services/api'
import { FaPlus, FaUserCheck, FaCheckCircle, FaTrophy, FaSignOutAlt, FaFileAlt } from 'react-icons/fa'
import './TableauDeBordFormateur.css'

function TableauDeBordFormateur() {
  const [ongletActif, setOngletActif] = useState('travaux')
  const [profil, setProfil] = useState(null)
  const [espaces, setEspaces] = useState([])
  const [livraisons, setLivraisons] = useState([])
  const [message, setMessage] = useState('')
  const [erreur, setErreur] = useState('')
  const [enCours, setEnCours] = useState(false)

  // Création travail
  const [idEspaceTravail, setIdEspaceTravail] = useState('')
  const [typeTravail, setTypeTravail] = useState('INDIVIDUAL')
  const [titre, setTitre] = useState('')
  const [consignes, setConsignes] = useState('')

  // Assignation
  const [idTravailAssigner, setIdTravailAssigner] = useState('')
  const [idProfilEtudiantAssigner, setIdProfilEtudiantAssigner] = useState('')

  // Évaluation
  const [idLivraison, setIdLivraison] = useState('')
  const [note, setNote] = useState(0)
  const [noteMax, setNoteMax] = useState(20)
  const [commentaire, setCommentaire] = useState('')
  const [publier, setPublier] = useState(false)

  // Classement
  const [idPromotionClassement, setIdPromotionClassement] = useState('')
  const [anneeClassement, setAnneeClassement] = useState(new Date().getFullYear())
  const [classement, setClassement] = useState(null)

  useEffect(() => {
    async function charger() {
      try {
        const [profilCourant, mesEspaces, mesLivraisons] = await Promise.all([
          recupererProfilConnecte(),
          listerMesEspacesFormateur(),
          listerLivraisonsAevaluer(),
        ])
        setProfil(profilCourant)
        setEspaces(mesEspaces)
        setLivraisons(mesLivraisons)
      } catch (e) {
        console.error(e)
        setErreur("Impossible de charger les données formateur.")
      }
    }
    charger()
  }, [])

  const espaceSelectionne = useMemo(
    () => espaces.find((e) => String(e.id) === String(idEspaceTravail)),
    [espaces, idEspaceTravail],
  )

  const etudiantsEspace = useMemo(() => {
    if (!espaceSelectionne) return []
    const details = espaceSelectionne.students_details || []
    return details.map((d) => ({ id: d.id, email: d.user__email }))
  }, [espaceSelectionne])

  async function handleCreerTravail(e) {
    e.preventDefault()
    setMessage('')
    setErreur('')
    setEnCours(true)
    try {
      const travail = await creerTravail({
        idEspace: idEspaceTravail,
        type: typeTravail,
        titre,
        consignes,
        dateLimite: null,
      })
      setMessage(`Travail créé avec succès (id ${travail.id}).`)
      setIdTravailAssigner(String(travail.id))
      setTitre('')
      setConsignes('')
    } catch (err) {
      console.error(err)
      setErreur("Erreur lors de la création du travail.")
    } finally {
      setEnCours(false)
    }
  }

  async function handleAssigner(e) {
    e.preventDefault()
    setMessage('')
    setErreur('')
    setEnCours(true)
    try {
      await assignerTravailIndividuel({
        idTravail: idTravailAssigner,
        idProfilEtudiant: idProfilEtudiantAssigner,
      })
      setMessage("Travail assigné avec succès.")
      setIdProfilEtudiantAssigner('')
    } catch (err) {
      console.error(err)
      setErreur("Erreur lors de l’assignation.")
    } finally {
      setEnCours(false)
    }
  }

  async function handleEvaluer(e) {
    e.preventDefault()
    setMessage('')
    setErreur('')
    setEnCours(true)
    try {
      await evaluerLivraison({
        idLivraison,
        note,
        noteMax,
        commentaire,
        publier,
      })
      setMessage("Évaluation enregistrée avec succès.")
      const mesLivraisons = await listerLivraisonsAevaluer()
      setLivraisons(mesLivraisons)
      setIdLivraison('')
      setCommentaire('')
      setPublier(false)
    } catch (err) {
      console.error(err)
      setErreur("Erreur lors de l’évaluation.")
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
    <div className="page-formateur">
      <aside className="sidebar">
        <div className="sidebar-entete">
          <h2>Formateur</h2>
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
            <FaCheckCircle /> Évaluations
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
            <h1>Espace Formateur</h1>
          </div>
        </header>

        {message && <div className="alerte alerte-succes">{message}</div>}
        {erreur && <div className="alerte alerte-erreur">{erreur}</div>}

        <section className="carte-directeur">
          <h2><FaPlus /> Créer un travail</h2>
          <form onSubmit={handleCreerTravail} className="formulaire">
        <label>
          Espace
          <select value={idEspaceTravail} onChange={(e) => setIdEspaceTravail(e.target.value)} required>
            <option value="">Sélectionner...</option>
            {espaces.map((es) => (
              <option key={es.id} value={es.id}>
                #{es.id} — {es.subject_code} ({es.year})
              </option>
            ))}
          </select>
        </label>

        <label>
          Type
          <select value={typeTravail} onChange={(e) => setTypeTravail(e.target.value)}>
            <option value="INDIVIDUAL">INDIVIDUEL</option>
            <option value="COLLECTIVE">COLLECTIF</option>
          </select>
        </label>

        <label>
          Titre
          <input value={titre} onChange={(e) => setTitre(e.target.value)} required />
        </label>

        <label>
          Consignes
          <textarea value={consignes} onChange={(e) => setConsignes(e.target.value)} required rows={4} />
        </label>

        <button disabled={enCours}>Créer</button>
          </form>
        </section>

        <section className="carte-directeur">
          <h2><FaUserCheck /> Assigner un travail individuel</h2>
          <form onSubmit={handleAssigner} className="formulaire">
        <label>
          Id du travail
          <input value={idTravailAssigner} onChange={(e) => setIdTravailAssigner(e.target.value)} required />
        </label>

        <label>
          Étudiant (profil inscrit dans l’espace)
          <select
            value={idProfilEtudiantAssigner}
            onChange={(e) => setIdProfilEtudiantAssigner(e.target.value)}
            required
          >
            <option value="">Sélectionner...</option>
            {etudiantsEspace.map((s) => (
              <option key={s.id} value={s.id}>
                Profil #{s.id} — {s.email}
              </option>
            ))}
          </select>
        </label>

        <button disabled={enCours}>Assigner</button>
          </form>
        </section>

        <section className="carte-directeur">
          <h2><FaCheckCircle /> Évaluer une livraison</h2>
          <p>Livraisons disponibles (mes espaces) : {livraisons.length}</p>
          <form onSubmit={handleEvaluer} className="formulaire">
        <label>
          Id de la livraison
          <input value={idLivraison} onChange={(e) => setIdLivraison(e.target.value)} required />
        </label>
        <label>
          Note
          <input type="number" value={note} onChange={(e) => setNote(Number(e.target.value))} required />
        </label>
        <label>
          Note maximale
          <input type="number" value={noteMax} onChange={(e) => setNoteMax(Number(e.target.value))} required />
        </label>
        <label>
          Commentaire
          <textarea value={commentaire} onChange={(e) => setCommentaire(e.target.value)} rows={3} />
        </label>
        <label>
          Publier l’évaluation
          <input type="checkbox" checked={publier} onChange={(e) => setPublier(e.target.checked)} />
        </label>
        <button disabled={enCours}>Enregistrer l’évaluation</button>
          </form>
        </section>

        <section className="carte-directeur">
          <h2><FaTrophy /> Classement</h2>
          <form onSubmit={handleClassement} className="formulaire">
        <label>
          Id promotion
          <input value={idPromotionClassement} onChange={(e) => setIdPromotionClassement(e.target.value)} required />
        </label>
        <label>
          Année
          <input type="number" value={anneeClassement} onChange={(e) => setAnneeClassement(e.target.value)} required />
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

export default TableauDeBordFormateur

