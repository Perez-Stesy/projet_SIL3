// ============================================
// GLOBAL STATE
// ============================================
let promotions = [];
let currentFilter = 'all';
let isEditMode = false;
let currentEditId = null;

// ============================================
// DOM ELEMENTS
// ============================================
const fabBtn = document.getElementById('fabBtn');
const createModal = document.getElementById('createModal');
const closeModal = document.getElementById('closeModal');
const cancelBtn = document.getElementById('cancelBtn');
const promotionForm = document.getElementById('promotionForm');
const promotionsGrid = document.getElementById('promotionsGrid');
const emptyState = document.getElementById('emptyState');
const toast = document.getElementById('toast');
const couleurInput = document.getElementById('couleur');
const couleurText = document.getElementById('couleur-text');
const filterBtns = document.querySelectorAll('.filter-btn');

// ============================================
// INITIALIZATION
// ============================================
document.addEventListener('DOMContentLoaded', () => {
    initializeEventListeners();
    loadPromotions();
    setupColorPicker();
    setupDateInputs();
});

// ============================================
// EVENT LISTENERS
// ============================================
function initializeEventListeners() {
    // Modal controls
    fabBtn.addEventListener('click', () => openModal());
    closeModal.addEventListener('click', () => closeModalFunc());
    cancelBtn.addEventListener('click', () => closeModalFunc());
    
    // Close modal on outside click
    createModal.addEventListener('click', (e) => {
        if (e.target === createModal) {
            closeModalFunc();
        }
    });
    
    // Form submission
    promotionForm.addEventListener('submit', handleFormSubmit);
    
    // Filter buttons
    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            currentFilter = btn.dataset.filter;
            renderPromotions();
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && createModal.classList.contains('active')) {
            closeModalFunc();
        }
        if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
            e.preventDefault();
            openModal();
        }
    });
}

function setupColorPicker() {
    couleurInput.addEventListener('input', (e) => {
        couleurText.value = e.target.value.toUpperCase();
    });
    
    couleurText.addEventListener('input', (e) => {
        const value = e.target.value;
        if (/^#[0-9A-Fa-f]{6}$/.test(value)) {
            couleurInput.value = value;
        }
    });
}

function setupDateInputs() {
    // Set default dates
    const today = new Date();
    const nextYear = new Date(today);
    nextYear.setFullYear(today.getFullYear() + 1);
    
    document.getElementById('date_debut').valueAsDate = today;
    document.getElementById('date_fin').valueAsDate = nextYear;
    
    // Set year input to current year
    document.getElementById('annee').value = today.getFullYear();
}

// ============================================
// MODAL FUNCTIONS
// ============================================
function openModal() {
    isEditMode = false;
    currentEditId = null;
    
    // Réinitialiser le formulaire
    promotionForm.reset();
    document.getElementById('promotionId').value = '';
    
    // Cacher le champ nombre d'étudiants
    document.getElementById('nombreEtudiantsGroup').style.display = 'none';
    document.getElementById('nombre_etudiants').required = false;
    
    // Réinitialiser le titre et le bouton
    document.getElementById('modalTitle').textContent = 'Créer une Nouvelle Promotion';
    document.getElementById('submitBtnText').textContent = 'Créer la Promotion';
    
    setupDateInputs();
    createModal.classList.add('active');
    document.body.style.overflow = 'hidden';
    document.getElementById('nom').focus();
}

function closeModalFunc() {
    createModal.classList.remove('active');
    document.body.style.overflow = '';
    promotionForm.reset();
    document.getElementById('promotionId').value = '';
    document.getElementById('nombreEtudiantsGroup').style.display = 'none';
    document.getElementById('nombre_etudiants').required = false;
    isEditMode = false;
    currentEditId = null;
}

// ============================================
// API FUNCTIONS
// ============================================
async function loadPromotions() {
    try {
        showLoading();
        const response = await fetch('/api/promotions/');
        const data = await response.json();
        
        if (response.ok) {
            promotions = data.promotions || [];
            renderPromotions();
        } else {
            showToast('Erreur lors du chargement des promotions', 'error');
        }
    } catch (error) {
        console.error('Error loading promotions:', error);
        showToast('Erreur de connexion au serveur', 'error');
    } finally {
        hideLoading();
    }
}

async function createPromotion(formData) {
    try {
        const data = {
            nom: formData.get('nom'),
            annee: parseInt(formData.get('annee')),
            description: formData.get('description'),
            date_debut: formData.get('date_debut'),
            date_fin: formData.get('date_fin'),
            nombre_etudiants: 0, // Toujours 0 à la création
            active: formData.get('active') === 'on',
            couleur: formData.get('couleur'),
        };
        
        const response = await fetch('/api/promotions/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast('Promotion créée avec succès !', 'success');
            closeModalFunc();
            loadPromotions();
            return true;
        } else {
            showToast(result.error || 'Erreur lors de la création', 'error');
            return false;
        }
    } catch (error) {
        console.error('Error creating promotion:', error);
        showToast('Erreur de connexion au serveur', 'error');
        return false;
    }
}

async function updatePromotion(id, formData) {
    try {
        const data = {
            nom: formData.get('nom'),
            annee: parseInt(formData.get('annee')),
            description: formData.get('description'),
            date_debut: formData.get('date_debut'),
            date_fin: formData.get('date_fin'),
            nombre_etudiants: parseInt(formData.get('nombre_etudiants')) || 0,
            active: formData.get('active') === 'on',
            couleur: formData.get('couleur'),
        };
        
        const response = await fetch(`/api/promotions/${id}/update/`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast('Promotion modifiée avec succès !', 'success');
            closeModalFunc();
            loadPromotions();
            return true;
        } else {
            showToast(result.error || 'Erreur lors de la modification', 'error');
            return false;
        }
    } catch (error) {
        console.error('Error updating promotion:', error);
        showToast('Erreur de connexion au serveur', 'error');
        return false;
    }
}

async function loadPromotionForEdit(id) {
    try {
        const response = await fetch(`/api/promotions/${id}/`);
        const result = await response.json();
        
        if (response.ok) {
            return result;
        } else {
            showToast(result.error || 'Erreur lors du chargement', 'error');
            return null;
        }
    } catch (error) {
        console.error('Error loading promotion:', error);
        showToast('Erreur de connexion au serveur', 'error');
        return null;
    }
}

function openEditModal(id) {
    isEditMode = true;
    currentEditId = id;
    
    // Charger les données de la promotion
    loadPromotionForEdit(id).then(promo => {
        if (promo) {
            // Remplir le formulaire
            document.getElementById('promotionId').value = promo.id;
            document.getElementById('nom').value = promo.nom;
            document.getElementById('annee').value = promo.annee;
            document.getElementById('description').value = promo.description || '';
            document.getElementById('date_debut').value = promo.date_debut;
            document.getElementById('date_fin').value = promo.date_fin;
            document.getElementById('nombre_etudiants').value = promo.nombre_etudiants;
            document.getElementById('active').checked = promo.active;
            document.getElementById('couleur').value = promo.couleur;
            document.getElementById('couleur-text').value = promo.couleur.toUpperCase();
            
            // Afficher le champ nombre d'étudiants
            document.getElementById('nombreEtudiantsGroup').style.display = 'block';
            document.getElementById('nombre_etudiants').required = true;
            
            // Changer le titre et le bouton
            document.getElementById('modalTitle').textContent = 'Modifier la Promotion';
            document.getElementById('submitBtnText').textContent = 'Modifier la Promotion';
            
            // Ouvrir le modal
            createModal.classList.add('active');
            document.body.style.overflow = 'hidden';
            document.getElementById('nom').focus();
        }
    });
}

async function deletePromotion(id) {
    if (!confirm('Êtes-vous sûr de vouloir supprimer cette promotion ?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/promotions/${id}/delete/`, {
            method: 'DELETE',
        });
        
        const result = await response.json();
        
        if (response.ok) {
            showToast('Promotion supprimée avec succès', 'success');
            loadPromotions();
        } else {
            showToast(result.error || 'Erreur lors de la suppression', 'error');
        }
    } catch (error) {
        console.error('Error deleting promotion:', error);
        showToast('Erreur de connexion au serveur', 'error');
    }
}

// ============================================
// FORM HANDLING
// ============================================
async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const submitBtn = form.querySelector('button[type="submit"]');
    const formData = new FormData(form);
    
    // Validation
    if (!formData.get('nom') || !formData.get('annee') || 
        !formData.get('date_debut') || !formData.get('date_fin')) {
        showToast('Veuillez remplir tous les champs requis', 'error');
        return;
    }
    
    // En mode édition, vérifier aussi le nombre d'étudiants
    if (isEditMode && (!formData.get('nombre_etudiants') || formData.get('nombre_etudiants') === '')) {
        showToast('Veuillez indiquer le nombre d\'étudiants inscrits', 'error');
        return;
    }
    
    // Disable button and show loading
    submitBtn.classList.add('loading');
    submitBtn.disabled = true;
    
    let success = false;
    if (isEditMode && currentEditId) {
        success = await updatePromotion(currentEditId, formData);
    } else {
        success = await createPromotion(formData);
    }
    
    // Re-enable button
    submitBtn.classList.remove('loading');
    submitBtn.disabled = false;
}

// ============================================
// RENDERING
// ============================================
function renderPromotions() {
    // Filter promotions
    let filteredPromotions = promotions;
    
    if (currentFilter === 'active') {
        filteredPromotions = promotions.filter(p => p.active);
    } else if (currentFilter === 'inactive') {
        filteredPromotions = promotions.filter(p => !p.active);
    }
    
    // Show empty state if no promotions
    if (filteredPromotions.length === 0) {
        promotionsGrid.style.display = 'none';
        emptyState.style.display = 'block';
        return;
    }
    
    // Hide empty state and show grid
    promotionsGrid.style.display = 'grid';
    emptyState.style.display = 'none';
    
    // Clear grid
    promotionsGrid.innerHTML = '';
    
    // Render each promotion
    filteredPromotions.forEach((promo, index) => {
        const card = createPromotionCard(promo, index);
        promotionsGrid.appendChild(card);
    });
}

function createPromotionCard(promo, index) {
    const card = document.createElement('div');
    card.className = 'promotion-card';
    card.style.setProperty('--card-color', promo.couleur);
    card.style.animationDelay = `${index * 0.1}s`;
    
    const dateDebut = new Date(promo.date_debut);
    const dateFin = new Date(promo.date_fin);
    const dateDebutStr = dateDebut.toLocaleDateString('fr-FR', { 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
    });
    const dateFinStr = dateFin.toLocaleDateString('fr-FR', { 
        day: 'numeric', 
        month: 'long', 
        year: 'numeric' 
    });
    
    let badges = '';
    if (promo.est_en_cours) {
        badges += '<span class="promotion-badge badge-en-cours">En cours</span>';
    } else if (promo.active) {
        badges += '<span class="promotion-badge badge-active">Active</span>';
    } else {
        badges += '<span class="promotion-badge badge-inactive">Inactive</span>';
    }
    
    card.innerHTML = `
        <div class="promotion-header">
            <div>
                <h3 class="promotion-title">${escapeHtml(promo.nom)}</h3>
                <p class="promotion-year">Année ${promo.annee}</p>
            </div>
            ${badges}
        </div>
        
        ${promo.description ? `<p class="promotion-description">${escapeHtml(promo.description)}</p>` : '<p class="promotion-description" style="color: #cbd5e1; font-style: italic;">Aucune description</p>'}
        
        <div class="promotion-details">
            <div class="detail-item">
                <span class="detail-label">Étudiants</span>
                <span class="detail-value">${promo.nombre_etudiants}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Durée</span>
                <span class="detail-value">${promo.duree_jours} jours</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Début</span>
                <span class="detail-value">${dateDebutStr}</span>
            </div>
            <div class="detail-item">
                <span class="detail-label">Fin</span>
                <span class="detail-value">${dateFinStr}</span>
            </div>
        </div>
        
        <div class="promotion-actions">
            <button class="action-btn btn-edit" onclick="openEditModal(${promo.id})">
                ✏️ Modifier
            </button>
            <button class="action-btn btn-delete" onclick="deletePromotion(${promo.id})">
                🗑️ Supprimer
            </button>
        </div>
    `;
    
    return card;
}

function showLoading() {
    promotionsGrid.innerHTML = `
        <div class="loading-state">
            <div class="spinner"></div>
            <p>Chargement des promotions...</p>
        </div>
    `;
    emptyState.style.display = 'none';
}

function hideLoading() {
    // Loading state is replaced by renderPromotions
}

// ============================================
// UTILITY FUNCTIONS
// ============================================
function showToast(message, type = 'success') {
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Make functions available globally for onclick handlers
window.deletePromotion = deletePromotion;
window.openEditModal = openEditModal;

