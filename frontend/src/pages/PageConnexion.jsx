import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { connexion, recupererProfilConnecte } from '../services/api'
import './PageConnexion.css'

function PageConnexion() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [motDePasse, setMotDePasse] = useState('')
  const [enCours, setEnCours] = useState(false)
  const [erreur, setErreur] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setErreur('')
    setEnCours(true)
    try {
      await connexion(email, motDePasse)
      const profil = await recupererProfilConnecte()
      
      // Log pour déboguer
      console.log('=== CONNEXION DEBUG ===')
      console.log('Profil complet:', profil)
      console.log('Rôle reçu:', profil.role)
      console.log('Type du rôle:', typeof profil.role)
      console.log('Rôle normalisé:', String(profil.role).toUpperCase().trim())

      // Normaliser le rôle pour éviter les problèmes de casse
      const role = String(profil.role || '').toUpperCase().trim()
      
      console.log('Redirection vers:', role)
      
      if (role === 'DIRECTEUR') {
        navigate('/directeur', { replace: true })
      } else if (role === 'FORMATEUR') {
        navigate('/formateur', { replace: true })
      } else if (role === 'ETUDIANT') {
        navigate('/etudiant', { replace: true })
      } else {
        console.error('Rôle inconnu ou manquant:', role)
        setErreur(`Rôle non reconnu: ${role || 'aucun'}`)
      }
    } catch (err) {
      console.error('Erreur de connexion:', err)
      console.error('Détails:', err.response?.data)
      
      // Afficher un message d'erreur plus détaillé
      const messageErreur = err.response?.data?.detail || 
                           err.response?.data?.message || 
                           err.message || 
                           "Identifiants invalides ou accès refusé."
      setErreur(messageErreur)
    } finally {
      setEnCours(false)
    }
  }

  return (
    <div className="page-centree">
      <div className="carte">
        <h1>Plateforme pédagogique</h1>

        <form onSubmit={handleSubmit} className="formulaire">
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
            Mot de passe
            <input
              type="password"
              value={motDePasse}
              onChange={(e) => setMotDePasse(e.target.value)}
              required
              placeholder="********"
            />
          </label>

          {erreur && <div className="alerte alerte-erreur">{erreur}</div>}

          <button type="submit" disabled={enCours}>
            {enCours ? 'Connexion en cours...' : 'Se connecter'}
          </button>
        </form>

        <p style={{ marginTop: '1rem', fontSize: '0.85rem' }}>
          Première connexion ?{' '}
          <a href="/activation" style={{ color: '#2563eb', fontWeight: '600' }}>
            Activer mon compte
          </a>
        </p>
      </div>
    </div>
  )
}

export default PageConnexion

