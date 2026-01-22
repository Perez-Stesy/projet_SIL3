import { Navigate } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { recupererProfilConnecte } from '../services/api'

function RouteProtegee({ children, requiredRole }) {
  const token = localStorage.getItem('token')
  const [profil, setProfil] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    async function verifierRole() {
      if (!token) {
        setLoading(false)
        return
      }
      try {
        const profilCourant = await recupererProfilConnecte()
        setProfil(profilCourant)
        
        // Normaliser le rôle (majuscules, sans espaces)
        const role = String(profilCourant.role).toUpperCase().trim()
        console.log('RouteProtegee - Rôle détecté:', role)
        console.log('RouteProtegee - Rôle requis:', requiredRole)
        console.log('RouteProtegee - Chemin actuel:', window.location.pathname)
        
        // Ne rediriger que si l'utilisateur n'est pas sur la bonne page ET que le requiredRole ne correspond pas
        const path = window.location.pathname
        if (requiredRole && role !== requiredRole.toUpperCase().trim()) {
          // L'utilisateur n'a pas le bon rôle pour cette page, rediriger selon son rôle
          console.log('Rôle incorrect pour cette page, redirection...')
          if (role === 'DIRECTEUR' && path !== '/directeur') {
            window.location.href = '/directeur'
            return
          }
          if (role === 'FORMATEUR' && path !== '/formateur') {
            window.location.href = '/formateur'
            return
          }
          if (role === 'ETUDIANT' && path !== '/etudiant') {
            window.location.href = '/etudiant'
            return
          }
        }
      } catch (err) {
        console.error('Erreur lors de la vérification du rôle:', err)
        localStorage.removeItem('token')
      } finally {
        setLoading(false)
      }
    }
    verifierRole()
  }, [token, requiredRole])

  if (!token) {
    return <Navigate to="/connexion" replace />
  }

  if (loading) {
    return <div>Chargement...</div>
  }

  // Normaliser les rôles pour la comparaison
  const roleProfil = profil ? String(profil.role || '').toUpperCase().trim() : null
  const roleRequis = requiredRole ? String(requiredRole).toUpperCase().trim() : null
  
  if (requiredRole && profil && roleProfil !== roleRequis) {
    console.log('RouteProtegee - Accès refusé:', {
      roleProfil,
      roleRequis,
      chemin: window.location.pathname
    })
    return <Navigate to="/connexion" replace />
  }

  return children
}

export default RouteProtegee

