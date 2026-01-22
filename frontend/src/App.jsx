import { Route, Routes, Navigate } from 'react-router-dom'
import './App.css'
import PageConnexion from './pages/PageConnexion'
import PageActivationCompte from './pages/PageActivationCompte'
import TableauDeBordDirecteur from './pages/TableauDeBordDirecteur'
import TableauDeBordFormateur from './pages/TableauDeBordFormateur'
import TableauDeBordEtudiant from './pages/TableauDeBordEtudiant'
import RouteProtegee from './components/RouteProtegee'

function App() {
  return (
    <Routes>
      <Route path="/connexion" element={<PageConnexion />} />
      <Route path="/activation" element={<PageActivationCompte />} />
      <Route
        path="/directeur"
        element={
          <RouteProtegee requiredRole="DIRECTEUR">
            <TableauDeBordDirecteur />
          </RouteProtegee>
        }
      />
      <Route
        path="/formateur"
        element={
          <RouteProtegee requiredRole="FORMATEUR">
            <TableauDeBordFormateur />
          </RouteProtegee>
        }
      />
      <Route
        path="/etudiant"
        element={
          <RouteProtegee requiredRole="ETUDIANT">
            <TableauDeBordEtudiant />
          </RouteProtegee>
        }
      />
      <Route path="*" element={<Navigate to="/connexion" replace />} />
    </Routes>
  )
}

export default App
