
import { useEffect, useState } from 'react'
import {
  creerCompteUtilisateur,
  creerEspace,
  creerMatiere,
  creerPromotion,
  affecterEtudiantPromotion,
  affecterFormateurEspace,
  ajouterEtudiantEspace,
  listerEspaces,
  listerMatieres,
  listerProfilsEtudiants,
  listerPromotions,
  listerUtilisateurs,
  recupererProfilConnecte,
} from '../services/api'
import { FaUserPlus, FaGraduationCap, FaBook, FaChalkboardTeacher, FaUserGraduate, FaUserTie, FaUsers } from 'react-icons/fa'
import './TableauDeBordDirecteur.css'

function TableauDeBordDirecteur() {
  const [ongletActif, setOngletActif] = useState('comptes')
  const [profil, setProfil] = useState(null)

  // Création de compte
  const [email, setEmail] = useState('')
  const [nom, setNom] = useState('')
  const [prenom, setPrenom] = useState('')
  const [sexe, setSexe] = useState('HOMME')
  const [role, setRole] = useState('FORMATEUR')
  const [enCours, setEnCours] = useState(false)
  const [messageSucces, setMessageSucces] = useState('')
  const [messageErreur, setMessageErreur] = useState('')

  // Promotions
  const [promotions, setPromotions] = useState([])
  const [nomPromotion, setNomPromotion] = useState('')
  const [anneePromotion, setAnneePromotion] = useState(new Date().getFullYear())

  // Matières
  const [matieres, setMatieres] = useState([])
  const [codeMatiere, setCodeMatiere] = useState('')
  const [nomMatiere, setNomMatiere] = useState('')

  // Espaces pédagogiques
  const [espaces, setEspaces] = useState([])
  const [idPromotionPourEspace, setIdPromotionPourEspace] = useState('')
  const [idMatierePourEspace, setIdMatierePourEspace] = useState('')
  const [anneeEspace, setAnneeEspace] = useState(new Date().getFullYear())

  // Affectations
  const [utilisateursEtudiants, setUtilisateursEtudiants] = useState([])
  const [utilisateursFormateurs, setUtilisateursFormateurs] = useState([])
  const [profilsEtudiants, setProfilsEtudiants] = useState([])

  const [idUtilisateurEtudiant, setIdUtilisateurEtudiant] = useState('')
  const [idPromotionPourEtudiant, setIdPromotionPourEtudiant] = useState('')

  const [idEspacePourFormateur, setIdEspacePourFormateur] = useState('')
  const [idUtilisateurFormateur, setIdUtilisateurFormateur] = useState('')

  const [idEspacePourEtudiant, setIdEspacePourEtudiant] = useState('')
  const [idProfilEtudiant, setIdProfilEtudiant] = useState('')

  const espaceSelectionnePourEtudiant = espaces.find(
    (e) => String(e.id) === String(idEspacePourEtudiant),
  )
  const profilsEtudiantsFiltresPourEspace = espaceSelectionnePourEtudiant
    ? profilsEtudiants.filter(
        (p) => String(p.promotion) === String(espaceSelectionnePourEtudiant.promotion),
      )
    : profilsEtudiants

  useEffect(() => {
    setMessageSucces('')
    setMessageErreur('')
  }, [email, nom, prenom, sexe, role, ongletActif])

  // Chargement initial des listes et du profil
  useEffect(() => {
    async function chargerDonnees() {
      try {
        const [profilCourant, promos, subs, spaces, etudiants, formateurs, profils] = await Promise.all([
          recupererProfilConnecte(),
          listerPromotions(),
          listerMatieres(),
          listerEspaces(),
          listerUtilisateurs({ role: 'ETUDIANT' }),
          listerUtilisateurs({ role: 'FORMATEUR' }),
          listerProfilsEtudiants(),
        ])
        setProfil(profilCourant)
        setPromotions(promos)
        setMatieres(subs)
        setEspaces(spaces)
        setUtilisateursEtudiants(etudiants)
        setUtilisateursFormateurs(formateurs)
        setProfilsEtudiants(profils)
      } catch (err) {
        console.error('Erreur lors du chargement des données', err)
      }
    }
    chargerDonnees()
  }, [])

  async function handleCreerCompte(e) {
    e.preventDefault()
    setMessageSucces('')
    setMessageErreur('')
    setEnCours(true)
    try {
      await creerCompteUtilisateur({ email, role, nom, prenom, sexe })
      setMessageSucces('Compte créé avec succès. L’utilisateur devra activer son compte.')
      setEmail('')
      setNom('')
      setPrenom('')
      setSexe('HOMME')
      setRole('FORMATEUR')
    } catch (err) {
      console.error(err)
      const msg =
        err.response?.data?.detail ||
        err.response?.data?.role ||
        err.response?.data?.email ||
        'Erreur lors de la création du compte.'
      setMessageErreur(
        typeof msg === 'string'
          ? msg
          : 'Erreur de validation, merci de vérifier les informations.',
      )
    } finally {
      setEnCours(false)
    }
  }

  async function handleCreerPromotion(e) {
    e.preventDefault()
    setMessageSucces('')
    setMessageErreur('')
    setEnCours(true)
    try {
      const promotionCreee = await creerPromotion({
        nom: nomPromotion,
        annee: Number(anneePromotion),
      })
      setPromotions((prev) => [promotionCreee, ...prev])
      setNomPromotion('')
      setMessageSucces('Promotion créée avec succès.')
    } catch (err) {
      console.error(err)
      setMessageErreur("Erreur lors de la création de la promotion.")
    } finally {
      setEnCours(false)
    }
  }

  async function handleCreerMatiere(e) {
    e.preventDefault()
    setMessageSucces('')
    setMessageErreur('')
    setEnCours(true)
    try {
      const matiereCreee = await creerMatiere({
        code: codeMatiere,
        nom: nomMatiere,
      })
      setMatieres((prev) => [matiereCreee, ...prev])
      setCodeMatiere('')
      setNomMatiere('')
      setMessageSucces('Matière créée avec succès.')
    } catch (err) {
      console.error(err)
      setMessageErreur("Erreur lors de la création de la matière.")
    } finally {
      setEnCours(false)
    }
  }

  async function handleCreerEspace(e) {
    e.preventDefault()
    setMessageSucces('')
    setMessageErreur('')
    setEnCours(true)
    try {
      const espaceCree = await creerEspace({
        idMatiere: idMatierePourEspace,
        annee: anneeEspace,
        idPromotion: idPromotionPourEspace,
      })
      setEspaces((prev) => [espaceCree, ...prev])
      setMessageSucces('Espace pédagogique créé avec succès.')
    } catch (err) {
      console.error(err)
      setMessageErreur("Erreur lors de la création de l’espace pédagogique.")
    } finally {
      setEnCours(false)
    }
  }

  async function handleAffecterEtudiantPromotion(e) {
    e.preventDefault()
    setMessageSucces('')
    setMessageErreur('')
    setEnCours(true)
    try {
      await affecterEtudiantPromotion({
        idUtilisateurEtudiant,
        idPromotion: idPromotionPourEtudiant,
      })
      const profils = await listerProfilsEtudiants()
      setProfilsEtudiants(profils)
      setMessageSucces("Étudiant affecté à la promotion avec succès.")
      setIdUtilisateurEtudiant('')
      setIdPromotionPourEtudiant('')
    } catch (err) {
      console.error(err)
      setMessageErreur("Erreur lors de l’affectation de l’étudiant à la promotion.")
    } finally {
      setEnCours(false)
    }
  }

  async function handleAffecterFormateurEspace(e) {
    e.preventDefault()
    setMessageSucces('')
    setMessageErreur('')
    setEnCours(true)
    try {
      await affecterFormateurEspace({
        idEspace: idEspacePourFormateur,
        idUtilisateurFormateur,
      })
      const spaces = await listerEspaces()
      setEspaces(spaces)
      setMessageSucces('Formateur affecté à l’espace avec succès.')
      setIdEspacePourFormateur('')
      setIdUtilisateurFormateur('')
    } catch (err) {
      console.error(err)
      setMessageErreur("Erreur lors de l’affectation du formateur à l’espace.")
    } finally {
      setEnCours(false)
    }
  }

  async function handleAjouterEtudiantEspace(e) {
    e.preventDefault()
    setMessageSucces('')
    setMessageErreur('')
    setEnCours(true)
    try {
      await ajouterEtudiantEspace({
        idEspace: idEspacePourEtudiant,
        idProfilEtudiant,
      })
      const spaces = await listerEspaces()
      setEspaces(spaces)
      setMessageSucces('Étudiant ajouté à l’espace avec succès.')
      setIdEspacePourEtudiant('')
      setIdProfilEtudiant('')
    } catch (err) {
      console.error(err)
      setMessageErreur("Erreur lors de l’ajout de l’étudiant à l’espace.")
    } finally {
      setEnCours(false)
    }
  }

  return (
    <div className="page-directeur">
      <aside className="sidebar">
        <div className="sidebar-entete">
          <h2>Directeur</h2>
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
            type="button"
            className={ongletActif === 'comptes' ? 'onglet actif' : 'onglet'}
            onClick={() => setOngletActif('comptes')}
          >
            Comptes
          </button>
          <button
            type="button"
            className={ongletActif === 'promotions' ? 'onglet actif' : 'onglet'}
            onClick={() => setOngletActif('promotions')}
          >
            Promotions
          </button>
          <button
            type="button"
            className={ongletActif === 'matieres' ? 'onglet actif' : 'onglet'}
            onClick={() => setOngletActif('matieres')}
          >
            Matières
          </button>
          <button
            type="button"
            className={ongletActif === 'espaces' ? 'onglet actif' : 'onglet'}
            onClick={() => setOngletActif('espaces')}
          >
            Espaces pédagogiques
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
          Déconnexion
        </button>
      </aside>

      <main className="contenu-directeur">
        <header className="entete">
          <div>
            <h1>Espace Directeur</h1>
          </div>
        </header>
        <div className="onglets">
          <button
            type="button"
            className={ongletActif === 'comptes' ? 'onglet actif' : 'onglet'}
            onClick={() => setOngletActif('comptes')}
          >
            Comptes
          </button>
          <button
            type="button"
            className={ongletActif === 'promotions' ? 'onglet actif' : 'onglet'}
            onClick={() => setOngletActif('promotions')}
          >
            Promotions
          </button>
          <button
            type="button"
            className={ongletActif === 'matieres' ? 'onglet actif' : 'onglet'}
            onClick={() => setOngletActif('matieres')}
          >
            Matières
          </button>
          <button
            type="button"
            className={ongletActif === 'espaces' ? 'onglet actif' : 'onglet'}
            onClick={() => setOngletActif('espaces')}
          >
            Espaces pédagogiques
          </button>
        </div>

        {ongletActif === 'comptes' && (
          <section className="carte-directeur">
            <h2><FaUserPlus /> Créer un compte</h2>
            <form onSubmit={handleCreerCompte} className="formulaire">
              <label>
                Nom
                <input
                  type="text"
                  value={nom}
                  onChange={(e) => setNom(e.target.value)}
                  required
                  placeholder="Dupont"
                />
              </label>

              <label>
                Prénom
                <input
                  type="text"
                  value={prenom}
                  onChange={(e) => setPrenom(e.target.value)}
                  required
                  placeholder="Jean"
                />
              </label>

              <label>
                Sexe
                <select value={sexe} onChange={(e) => setSexe(e.target.value)}>
                  <option value="HOMME">Homme</option>
                  <option value="FEMME">Femme</option>
                  <option value="AUTRE">Autre</option>
                </select>
              </label>

              <label>
                Adresse e-mail
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  required
                  placeholder="exemple@domaine.com"
                />
              </label>

              <label>
                Rôle
                <select value={role} onChange={(e) => setRole(e.target.value)}>
                  <option value="FORMATEUR">FORMATEUR</option>
                  <option value="ETUDIANT">ETUDIANT</option>
                </select>
              </label>

              {messageSucces && <div className="alerte alerte-succes">{messageSucces}</div>}
              {messageErreur && <div className="alerte alerte-erreur">{messageErreur}</div>}

              <button type="submit" disabled={enCours}>
                {enCours ? 'Création en cours...' : 'Créer le compte'}
              </button>
            </form>
          </section>
        )}

        {ongletActif === 'promotions' && (
          <section className="carte-directeur">
            <h2><FaGraduationCap /> Promotions</h2>

            <form onSubmit={handleCreerPromotion} className="formulaire">
              <label>
                Nom de la promotion
                <input
                  type="text"
                  value={nomPromotion}
                  onChange={(e) => setNomPromotion(e.target.value)}
                  required
                  placeholder="L1 Informatique"
                />
              </label>

              <label>
                Année
                <input
                  type="number"
                  value={anneePromotion}
                  onChange={(e) => setAnneePromotion(e.target.value)}
                  required
                />
              </label>

              {messageSucces && <div className="alerte alerte-succes">{messageSucces}</div>}
              {messageErreur && <div className="alerte alerte-erreur">{messageErreur}</div>}

              <button type="submit" disabled={enCours}>
                {enCours ? 'Création en cours...' : 'Créer la promotion'}
              </button>
            </form>

            <h3 className="titre-liste">Promotions existantes</h3>
            <div className="liste-simple">
              {promotions.length === 0 && <p>Aucune promotion pour le moment.</p>}
              {promotions.map((promo) => (
                <div key={promo.id} className="ligne-liste">
                  <span>{promo.name}</span>
                  <span className="badge">{promo.year}</span>
                </div>
              ))}
            </div>

            <h3 className="titre-liste"><FaUserGraduate /> Affecter un étudiant à une promotion</h3>
            <form onSubmit={handleAffecterEtudiantPromotion} className="formulaire">
              <label>
                Étudiant (utilisateur)
                <select
                  value={idUtilisateurEtudiant}
                  onChange={(e) => setIdUtilisateurEtudiant(e.target.value)}
                  required
                >
                  <option value="">Sélectionner...</option>
                  {utilisateursEtudiants.map((u) => (
                    <option key={u.id} value={u.id}>
                      #{u.id} — {u.email}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Promotion
                <select
                  value={idPromotionPourEtudiant}
                  onChange={(e) => setIdPromotionPourEtudiant(e.target.value)}
                  required
                >
                  <option value="">Sélectionner...</option>
                  {promotions.map((promo) => (
                    <option key={promo.id} value={promo.id}>
                      {promo.name} ({promo.year})
                    </option>
                  ))}
                </select>
              </label>

              {messageSucces && <div className="alerte alerte-succes">{messageSucces}</div>}
              {messageErreur && <div className="alerte alerte-erreur">{messageErreur}</div>}

              <button type="submit" disabled={enCours}>
                {enCours ? 'Affectation en cours...' : 'Affecter'}
              </button>
            </form>

            <h3 className="titre-liste">Profils étudiants affectés</h3>
            <div className="liste-simple">
              {profilsEtudiants.length === 0 && <p>Aucun étudiant affecté pour le moment.</p>}
              {profilsEtudiants.map((p) => (
                <div key={p.id} className="ligne-liste">
                  <span>
                    Profil #{p.id} — {p.email}
                  </span>
                  <span className="badge">Promotion #{p.promotion}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {ongletActif === 'matieres' && (
          <section className="carte-directeur">
            <h2><FaBook /> Matières</h2>

            <form onSubmit={handleCreerMatiere} className="formulaire">
              <label>
                Code
                <input
                  type="text"
                  value={codeMatiere}
                  onChange={(e) => setCodeMatiere(e.target.value)}
                  required
                  placeholder="MATH101"
                />
              </label>

              <label>
                Nom
                <input
                  type="text"
                  value={nomMatiere}
                  onChange={(e) => setNomMatiere(e.target.value)}
                  required
                  placeholder="Analyse 1"
                />
              </label>

              {messageSucces && <div className="alerte alerte-succes">{messageSucces}</div>}
              {messageErreur && <div className="alerte alerte-erreur">{messageErreur}</div>}

              <button type="submit" disabled={enCours}>
                {enCours ? 'Création en cours...' : 'Créer la matière'}
              </button>
            </form>

            <h3 className="titre-liste">Matières existantes</h3>
            <div className="liste-simple">
              {matieres.length === 0 && <p>Aucune matière pour le moment.</p>}
              {matieres.map((m) => (
                <div key={m.id} className="ligne-liste">
                  <span className="badge">{m.code}</span>
                  <span>{m.name}</span>
                </div>
              ))}
            </div>
          </section>
        )}

        {ongletActif === 'espaces' && (
          <section className="carte-directeur">
            <h2><FaChalkboardTeacher /> Espaces pédagogiques</h2>

            <form onSubmit={handleCreerEspace} className="formulaire">
              <label>
                Promotion
                <select
                  value={idPromotionPourEspace}
                  onChange={(e) => setIdPromotionPourEspace(e.target.value)}
                  required
                >
                  <option value="">Sélectionner...</option>
                  {promotions.map((promo) => (
                    <option key={promo.id} value={promo.id}>
                      {promo.name} ({promo.year})
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Matière
                <select
                  value={idMatierePourEspace}
                  onChange={(e) => setIdMatierePourEspace(e.target.value)}
                  required
                >
                  <option value="">Sélectionner...</option>
                  {matieres.map((m) => (
                    <option key={m.id} value={m.id}>
                      {m.code} - {m.name}
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Année
                <input
                  type="number"
                  value={anneeEspace}
                  onChange={(e) => setAnneeEspace(e.target.value)}
                  required
                />
              </label>

              {messageSucces && <div className="alerte alerte-succes">{messageSucces}</div>}
              {messageErreur && <div className="alerte alerte-erreur">{messageErreur}</div>}

              <button type="submit" disabled={enCours}>
                {enCours ? 'Création en cours...' : 'Créer l’espace pédagogique'}
              </button>
            </form>

            <h3 className="titre-liste">Espaces existants</h3>
            <div className="liste-simple">
              {espaces.length === 0 && <p>Aucun espace pédagogique pour le moment.</p>}
              {espaces.map((espace) => (
                <div key={espace.id} className="ligne-liste">
                  <span>
                    {espace.subject_name || espace.subject} — {espace.promotion_name || espace.promotion}
                  </span>
                  <span className="badge">{espace.year}</span>
                </div>
              ))}
            </div>

            <h3 className="titre-liste"><FaUserTie /> Affecter un formateur à un espace</h3>
            <form onSubmit={handleAffecterFormateurEspace} className="formulaire">
              <label>
                Espace
                <select
                  value={idEspacePourFormateur}
                  onChange={(e) => setIdEspacePourFormateur(e.target.value)}
                  required
                >
                  <option value="">Sélectionner...</option>
                  {espaces.map((espace) => (
                    <option key={espace.id} value={espace.id}>
                      #{espace.id} — {espace.subject_code || espace.subject} ({espace.year})
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Formateur (utilisateur)
                <select
                  value={idUtilisateurFormateur}
                  onChange={(e) => setIdUtilisateurFormateur(e.target.value)}
                  required
                >
                  <option value="">Sélectionner...</option>
                  {utilisateursFormateurs.map((u) => (
                    <option key={u.id} value={u.id}>
                      #{u.id} — {u.email}
                    </option>
                  ))}
                </select>
              </label>

              {messageSucces && <div className="alerte alerte-succes">{messageSucces}</div>}
              {messageErreur && <div className="alerte alerte-erreur">{messageErreur}</div>}

              <button type="submit" disabled={enCours}>
                {enCours ? 'Affectation en cours...' : 'Affecter le formateur'}
              </button>
            </form>

            <h3 className="titre-liste"><FaUsers /> Ajouter un étudiant à un espace</h3>
            <form onSubmit={handleAjouterEtudiantEspace} className="formulaire">
              <label>
                Espace
                <select
                  value={idEspacePourEtudiant}
                  onChange={(e) => {
                    setIdEspacePourEtudiant(e.target.value)
                    setIdProfilEtudiant('')
                  }}
                  required
                >
                  <option value="">Sélectionner...</option>
                  {espaces.map((espace) => (
                    <option key={espace.id} value={espace.id}>
                      #{espace.id} — {espace.subject_code || espace.subject} ({espace.year})
                    </option>
                  ))}
                </select>
              </label>

              <label>
                Étudiant (profil)
                <select
                  value={idProfilEtudiant}
                  onChange={(e) => setIdProfilEtudiant(e.target.value)}
                  required
                >
                  <option value="">Sélectionner...</option>
                  {profilsEtudiantsFiltresPourEspace.map((p) => (
                    <option key={p.id} value={p.id}>
                      Profil #{p.id} — {p.email}
                    </option>
                  ))}
                </select>
              </label>

              {messageSucces && <div className="alerte alerte-succes">{messageSucces}</div>}
              {messageErreur && <div className="alerte alerte-erreur">{messageErreur}</div>}

              <button type="submit" disabled={enCours}>
                {enCours ? 'Ajout en cours...' : "Ajouter l’étudiant"}
              </button>
            </form>
          </section>
        )}
      </main>
    </div>
  )
}

export default TableauDeBordDirecteur

