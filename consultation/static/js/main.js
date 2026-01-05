const API_BASE_URL = '/api';

// Charger la liste des étudiants au chargement de la page
document.addEventListener('DOMContentLoaded', function() {
    chargerListeEtudiants();
    
    // Permettre la recherche avec la touche Entrée
    const numeroInput = document.getElementById('numeroEtudiant');
    if (numeroInput) {
        numeroInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                chercherTravaux();
            }
        });
    }
});

/**
 * Charge la liste de tous les étudiants dans le select
 */
async function chargerListeEtudiants() {
    try {
        const response = await fetch(`${API_BASE_URL}/etudiants/`);
        const data = await response.json();
        
        const select = document.getElementById('selectEtudiant');
        select.innerHTML = '<option value="">-- Sélectionner un étudiant --</option>';
        
        data.etudiants.forEach(etudiant => {
            const option = document.createElement('option');
            option.value = etudiant.id;
            option.textContent = `${etudiant.prenom} ${etudiant.nom} (${etudiant.numero_etudiant})`;
            select.appendChild(option);
        });
    } catch (error) {
        console.error('Erreur lors du chargement des étudiants:', error);
    }
}

/**
 * Recherche les travaux par numéro d'étudiant
 */
async function chercherTravaux() {
    const numeroEtudiant = document.getElementById('numeroEtudiant').value.trim();
    const errorMessage = document.getElementById('errorMessage');
    
    // Réinitialiser les messages d'erreur
    errorMessage.textContent = '';
    
    if (!numeroEtudiant) {
        errorMessage.textContent = 'Veuillez entrer un numéro d\'étudiant';
        return;
    }
    
    afficherChargement(true);
    cacherResultats();
    
    try {
        const response = await fetch(`${API_BASE_URL}/etudiants/${numeroEtudiant}/travaux/`);
        
        if (response.status === 404) {
            throw new Error('Étudiant non trouvé');
        }
        
        if (!response.ok) {
            throw new Error('Erreur lors de la récupération des données');
        }
        
        const data = await response.json();
        afficherResultats(data);
    } catch (error) {
        errorMessage.textContent = error.message || 'Une erreur est survenue';
        afficherChargement(false);
    }
}

/**
 * Charge les travaux lorsqu'un étudiant est sélectionné dans le select
 */
async function chargerTravauxParSelect() {
    const select = document.getElementById('selectEtudiant');
    const etudiantId = select.value;
    const errorMessage = document.getElementById('errorMessage');
    
    errorMessage.textContent = '';
    
    if (!etudiantId) {
        cacherResultats();
        return;
    }
    
    afficherChargement(true);
    cacherResultats();
    
    try {
        const response = await fetch(`${API_BASE_URL}/etudiants/${etudiantId}/travaux/`);
        
        if (response.status === 404) {
            throw new Error('Étudiant non trouvé');
        }
        
        if (!response.ok) {
            throw new Error('Erreur lors de la récupération des données');
        }
        
        const data = await response.json();
        afficherResultats(data);
        
        // Mettre à jour le champ de recherche avec le numéro d'étudiant
        document.getElementById('numeroEtudiant').value = data.etudiant.numero_etudiant;
    } catch (error) {
        errorMessage.textContent = error.message || 'Une erreur est survenue';
        afficherChargement(false);
    }
}

/**
 * Affiche les résultats (informations de l'étudiant et travaux)
 */
function afficherResultats(data) {
    afficherChargement(false);
    
    // Afficher les informations de l'étudiant
    const etudiantInfo = document.getElementById('etudiantInfo');
    document.getElementById('nomComplet').textContent = `${data.etudiant.prenom} ${data.etudiant.nom}`;
    document.getElementById('numeroEtudiantInfo').textContent = data.etudiant.numero_etudiant;
    document.getElementById('emailInfo').textContent = data.etudiant.email;
    etudiantInfo.style.display = 'block';
    
    // Afficher les travaux
    const travauxSection = document.getElementById('travauxSection');
    const travauxList = document.getElementById('travauxList');
    const noTravaux = document.getElementById('noTravaux');
    
    if (data.travaux && data.travaux.length > 0) {
        travauxList.innerHTML = '';
        data.travaux.forEach((travail, index) => {
            const card = creerCarteTravail(travail, index);
            travauxList.appendChild(card);
        });
        travauxSection.style.display = 'block';
        noTravaux.style.display = 'none';
    } else {
        travauxSection.style.display = 'block';
        noTravaux.style.display = 'block';
        travauxList.innerHTML = '';
    }
}

/**
 * Crée une carte HTML pour afficher un travail
 */
function creerCarteTravail(travail, index) {
    const card = document.createElement('div');
    card.className = 'travail-card';
    card.style.animationDelay = `${index * 0.1}s`;
    
    const statutClass = `statut-${travail.statut}`;
    
    card.innerHTML = `
        <div class="travail-header">
            <div class="travail-titre">${escapeHtml(travail.titre)}</div>
            <span class="statut-badge ${statutClass}">${escapeHtml(travail.statut_display)}</span>
        </div>
        <div class="travail-description">${escapeHtml(travail.description)}</div>
        <div class="travail-details">
            <div class="detail-item">
                <span class="detail-label">Date d'assignation</span>
                <span class="detail-value">${formaterDate(travail.date_assignation)}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Date limite</span>
                <span class="detail-value">${formaterDate(travail.date_limite)}</span>
            </div>
        </div>
        ${travail.note !== null ? `
            <div class="note-section">
                <span class="detail-label">Note</span>
                <div class="note-value">${travail.note}/20</div>
            </div>
        ` : ''}
        ${travail.commentaire ? `
            <div class="commentaire-section">
                <span class="detail-label">Commentaire</span>
                <div class="commentaire-text">${escapeHtml(travail.commentaire)}</div>
            </div>
        ` : ''}
    `;
    
    return card;
}

/**
 * Formate une date au format français
 */
function formaterDate(dateString) {
    const date = new Date(dateString);
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return date.toLocaleDateString('fr-FR', options);
}

/**
 * Échappe les caractères HTML pour éviter les injections XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Affiche ou cache l'indicateur de chargement
 */
function afficherChargement(afficher) {
    document.getElementById('loading').style.display = afficher ? 'block' : 'none';
}

/**
 * Cache tous les résultats
 */
function cacherResultats() {
    document.getElementById('etudiantInfo').style.display = 'none';
    document.getElementById('travauxSection').style.display = 'none';
}


