import { useState } from 'react'
import { activerCompte } from '../services/api'
import './PageConnexion.css'

function PageActivationCompte() {
  const [email, setEmail] = useState('')
  const [motDePasse, setMotDePasse] = useState('')
  const [confirmation, setConfirmation] = useState('')
  const [enCours, setEnCours] = useState(false)
  const [message, setMessage] = useState('')
  const [erreur, setErreur] = useState('')

  async function handleSubmit(e) {
    e.preventDefault()
    setMessage('')
    setErreur('')
    setEnCours(true)
    try {
      await activerCompte({ email, motDePasse, confirmation })
      setMessage('Mot de passe défini avec succès. Vous pouvez maintenant vous connecter.')
      setMotDePasse('')
      setConfirmation('')
    } catch (err) {
      console.error(err)
      const msg =
        err.response?.data?.email ||
        err.response?.data?.password_confirmation ||
        err.response?.data?.detail ||
        'Erreur lors de l’activation du compte.'
      setErreur(typeof msg === 'string' ? msg : 'Erreur lors de l’activation du compte.')
    } finally {
      setEnCours(false)
    }
  }

  return (
    <div className="page-centree">
      <div className="carte">
        <h1>Activation de compte</h1>
        <p className="sous-titre">
          Première connexion : définissez votre mot de passe à partir de votre adresse e-mail.
        </p>

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
            Nouveau mot de passe
            <input
              type="password"
              value={motDePasse}
              onChange={(e) => setMotDePasse(e.target.value)}
              required
              placeholder="********"
            />
          </label>

          <label>
            Confirmer le mot de passe
            <input
              type="password"
              value={confirmation}
              onChange={(e) => setConfirmation(e.target.value)}
              required
              placeholder="********"
            />
          </label>

          {message && <div className="alerte alerte-succes">{message}</div>}
          {erreur && <div className="alerte alerte-erreur">{erreur}</div>}

          <button type="submit" disabled={enCours}>
            {enCours ? 'Activation en cours...' : 'Activer mon compte'}
          </button>
        </form>
      </div>
    </div>
  )
}

export default PageActivationCompte

