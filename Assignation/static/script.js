const API_BASE_URL = '/api';

// Éléments du DOM
const assignmentForm = document.getElementById('assignmentForm');
const studentForm = document.getElementById('studentForm');
const etudiantSelect = document.getElementById('etudiantSelect');
const filterEtudiant = document.getElementById('filterEtudiant');
const assignmentsList = document.getElementById('assignmentsList');
const emptyState = document.getElementById('emptyState');
const refreshBtn = document.getElementById('refreshBtn');
const messageDiv = document.getElementById('message');

// Fonction utilitaire pour afficher les messages
function showMessage(text, type = 'info') {
    messageDiv.textContent = text;
    messageDiv.className = `message ${type}`;
    messageDiv.classList.add('show');
    
    setTimeout(() => {
        messageDiv.classList.remove('show');
    }, 3000);
}

// Charger la liste des étudiants
async function loadEtudiants() {
    try {
        const response = await fetch(`${API_BASE_URL}/etudiants/`);
        if (!response.ok) throw new Error('Erreur lors du chargement des étudiants');
        
        const etudiants = await response.json();
        
        // Remplir le select pour assigner un travail
        etudiantSelect.innerHTML = '<option value="">-- Sélectionner un étudiant --</option>';
        etudiants.forEach(etudiant => {
            const option = document.createElement('option');
            option.value = etudiant.id;
            option.textContent = `${etudiant.prenom} ${etudiant.nom} (${etudiant.numero_etudiant})`;
            etudiantSelect.appendChild(option);
        });
        
        // Remplir le select de filtre
        filterEtudiant.innerHTML = '<option value="">-- Tous les étudiants --</option>';
        etudiants.forEach(etudiant => {
            const option = document.createElement('option');
            option.value = etudiant.id;
            option.textContent = `${etudiant.prenom} ${etudiant.nom}`;
            filterEtudiant.appendChild(option);
        });
        
        return etudiants;
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors du chargement des étudiants', 'error');
        return [];
    }
}

// Charger la liste des travaux
async function loadTravaux() {
    try {
        const filterValue = filterEtudiant.value;
        let url = `${API_BASE_URL}/travaux/`;
        
        if (filterValue) {
            url = `${API_BASE_URL}/travaux/par_etudiant/?etudiant_id=${filterValue}`;
        }
        
        const response = await fetch(url);
        if (!response.ok) throw new Error('Erreur lors du chargement des travaux');
        
        const travaux = await response.json();
        displayTravaux(travaux);
    } catch (error) {
        console.error('Erreur:', error);
        showMessage('Erreur lors du chargement des travaux', 'error');
    }
}

// Afficher les travaux dans la liste
function displayTravaux(travaux) {
    assignmentsList.innerHTML = '';
    
    if (travaux.length === 0) {
        emptyState.style.display = 'block';
        return;
    }
    
    emptyState.style.display = 'none';
    
    travaux.forEach(travail => {
        const card = document.createElement('div');
        card.className = 'assignment-card';
        
        const dateLimite = new Date(travail.date_limite);
        const dateFormatee = dateLimite.toLocaleDateString('fr-FR', {
            day: '2-digit',
            month: '2-digit',
            year: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
        
        const statutLabels = {
            'en_attente': 'En attente',
            'en_cours': 'En cours',
            'termine': 'Terminé'
        };
        
        card.innerHTML = `
            <h3>${escapeHtml(travail.titre)}</h3>
            <div class="student-info">
                👤 ${escapeHtml(travail.etudiant_nom || travail.etudiant_detail?.prenom + ' ' + travail.etudiant_detail?.nom)}
            </div>
            <div class="description">${escapeHtml(travail.description)}</div>
            <div class="meta">
                <span class="date">📅 Limite: ${dateFormatee}</span>
                <span class="statut statut-${travail.statut}">${statutLabels[travail.statut] || travail.statut}</span>
            </div>
        `;
        
        assignmentsList.appendChild(card);
    });
}

// Fonction pour échapper le HTML (sécurité)
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Gérer la soumission du formulaire d'assignation
assignmentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        titre: document.getElementById('titre').value,
        description: document.getElementById('description').value,
        date_limite: document.getElementById('dateLimite').value,
        etudiant: parseInt(etudiantSelect.value),
        statut: document.getElementById('statut').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/travaux/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erreur lors de l\'assignation');
        }
        
        showMessage('Travail assigné avec succès!', 'success');
        assignmentForm.reset();
        loadTravaux();
    } catch (error) {
        console.error('Erreur:', error);
        showMessage(error.message || 'Erreur lors de l\'assignation du travail', 'error');
    }
});

// Gérer la soumission du formulaire d'étudiant
studentForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const formData = {
        nom: document.getElementById('nom').value,
        prenom: document.getElementById('prenom').value,
        email: document.getElementById('email').value,
        numero_etudiant: document.getElementById('numeroEtudiant').value
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/etudiants/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Erreur lors de l\'ajout de l\'étudiant');
        }
        
        showMessage('Étudiant ajouté avec succès!', 'success');
        studentForm.reset();
        await loadEtudiants();
    } catch (error) {
        console.error('Erreur:', error);
        showMessage(error.message || 'Erreur lors de l\'ajout de l\'étudiant', 'error');
    }
});

// Gérer le filtre par étudiant
filterEtudiant.addEventListener('change', () => {
    loadTravaux();
});

// Bouton d'actualisation
refreshBtn.addEventListener('click', () => {
    loadTravaux();
    showMessage('Liste actualisée', 'info');
});

// Initialisation au chargement de la page
document.addEventListener('DOMContentLoaded', async () => {
    await loadEtudiants();
    loadTravaux();
});
