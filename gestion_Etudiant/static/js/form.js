// Form JavaScript with real-time preview and validation

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('studentForm');
    const moyenneInput = document.getElementById('id_moyenne_generale');
    const moyenneSlider = document.getElementById('moyenneSlider');
    const promotionSelect = document.getElementById('promotion-select');
    
    // Preview elements
    const previewName = document.getElementById('previewName');
    const previewPromotion = document.getElementById('previewPromotion');
    const previewMoyenne = document.getElementById('previewMoyenne');
    const previewCard = document.getElementById('previewCard');
    const previewRanking = document.getElementById('previewRanking');
    const previewRank = document.getElementById('previewRank');
    const previewNote = document.getElementById('previewNote');
    
    // Sync slider with input
    if (moyenneInput && moyenneSlider) {
        moyenneSlider.addEventListener('input', function() {
            moyenneInput.value = this.value;
            updatePreview();
            animateMoyenneChange();
        });

        moyenneInput.addEventListener('input', function() {
            moyenneSlider.value = this.value;
            updatePreview();
            animateMoyenneChange();
        });

        // Initialize slider value
        if (moyenneInput.value) {
            moyenneSlider.value = moyenneInput.value;
        }
    }

    // Real-time preview updates
    const formInputs = form.querySelectorAll('input, select');
    formInputs.forEach(input => {
        input.addEventListener('input', updatePreview);
        input.addEventListener('change', updatePreview);
        
        // Add focus animation
        input.addEventListener('focus', function() {
            this.parentElement.style.transform = 'scale(1.02)';
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.style.transform = 'scale(1)';
        });
    });

    function updatePreview() {
        const nom = document.getElementById('id_nom')?.value || '';
        const prenom = document.getElementById('id_prenom')?.value || '';
        const promotion = promotionSelect?.selectedOptions[0]?.text || '';
        const promotionId = promotionSelect?.value || '';
        const moyenne = moyenneInput?.value || '0';
        
        if (nom || prenom) {
            previewName.textContent = `${prenom} ${nom}`.trim() || '-';
        } else {
            previewName.textContent = '-';
        }
        
        previewPromotion.textContent = promotion || '-';
        previewMoyenne.textContent = moyenne ? parseFloat(moyenne).toFixed(2) : '0.00';
        
        // Estimate ranking if promotion and moyenne are provided
        if (promotionId && moyenne && parseFloat(moyenne) > 0) {
            estimateRanking(promotionId, parseFloat(moyenne));
        } else {
            previewRanking.style.display = 'none';
            previewNote.style.display = 'none';
        }
        
        // Animate preview card
        previewCard.style.animation = 'none';
        setTimeout(() => {
            previewCard.style.animation = 'pulse 0.5s ease';
        }, 10);
    }

    async function estimateRanking(promotionId, moyenne) {
        try {
            const response = await fetch(`/api/promotion/${promotionId}/classement/`);
            if (response.ok) {
                const data = await response.json();
                const etudiants = data.etudiants || [];
                
                // Count students with higher moyenne
                let rank = 1;
                for (const etudiant of etudiants) {
                    if (etudiant.moyenne_generale > moyenne) {
                        rank++;
                    } else {
                        break;
                    }
                }
                
                const totalStudents = etudiants.length;
                const estimatedRank = rank;
                const totalAfter = totalStudents + 1;
                
                previewRank.innerHTML = `<span style="font-size: 1.5rem;">${estimatedRank}ᵉ</span> / ${totalAfter}`;
                previewRanking.style.display = 'flex';
                previewNote.style.display = 'block';
                
                // Add visual indicator
                if (estimatedRank <= 3) {
                    previewRanking.style.borderColor = 'rgba(255, 215, 0, 0.5)';
                } else {
                    previewRanking.style.borderColor = 'rgba(255, 255, 255, 0.3)';
                }
            }
        } catch (error) {
            console.error('Error estimating ranking:', error);
            previewRanking.style.display = 'none';
        }
    }

    function animateMoyenneChange() {
        const moyenneValue = parseFloat(moyenneInput.value) || 0;
        const percentage = (moyenneValue / 20) * 100;
        
        // Add visual feedback
        if (moyenneValue >= 16) {
            moyenneInput.style.borderColor = '#4ade80';
        } else if (moyenneValue >= 12) {
            moyenneInput.style.borderColor = '#fbbf24';
        } else if (moyenneValue >= 10) {
            moyenneInput.style.borderColor = '#f59e0b';
        } else {
            moyenneInput.style.borderColor = 'rgba(255, 255, 255, 0.2)';
        }
    }

    // Form submission with loading state
    form.addEventListener('submit', function(e) {
        const submitBtn = form.querySelector('.btn-submit');
        if (submitBtn) {
            submitBtn.classList.add('loading');
            submitBtn.disabled = true;
        }
        
        // Validate form before submission
        if (!validateForm()) {
            e.preventDefault();
            if (submitBtn) {
                submitBtn.classList.remove('loading');
                submitBtn.disabled = false;
            }
            return false;
        }
    });

    function validateForm() {
        let isValid = true;
        const requiredFields = form.querySelectorAll('[required]');
        
        requiredFields.forEach(field => {
            if (!field.value.trim()) {
                isValid = false;
                field.style.borderColor = '#ef4444';
                field.style.animation = 'shake 0.5s ease';
                
                setTimeout(() => {
                    field.style.borderColor = '';
                    field.style.animation = '';
                }, 500);
            }
        });

        // Validate email format
        const emailField = document.getElementById('id_email');
        if (emailField && emailField.value) {
            const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
            if (!emailRegex.test(emailField.value)) {
                isValid = false;
                emailField.style.borderColor = '#ef4444';
                showError(emailField, 'Format email invalide');
            }
        }

        // Validate moyenne range
        if (moyenneInput && moyenneInput.value) {
            const moyenne = parseFloat(moyenneInput.value);
            if (moyenne < 0 || moyenne > 20) {
                isValid = false;
                moyenneInput.style.borderColor = '#ef4444';
                showError(moyenneInput, 'La moyenne doit être entre 0 et 20');
            }
        }

        return isValid;
    }

    function showError(field, message) {
        // Remove existing error
        const existingError = field.parentElement.querySelector('.error-message');
        if (existingError) {
            existingError.remove();
        }

        // Add new error
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        field.parentElement.appendChild(errorDiv);

        // Remove error after 3 seconds
        setTimeout(() => {
            errorDiv.remove();
            field.style.borderColor = '';
        }, 3000);
    }

    // Initial preview update
    updatePreview();

    // Add typing effect to preview
    let typingTimeout;
    formInputs.forEach(input => {
        input.addEventListener('input', function() {
            clearTimeout(typingTimeout);
            typingTimeout = setTimeout(updatePreview, 300);
        });
    });

    // Animate form on load
    const formGroups = form.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        setTimeout(() => {
            group.style.transition = 'all 0.5s ease';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, index * 100);
    });
});

