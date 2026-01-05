// Ranking page JavaScript with animations

document.addEventListener('DOMContentLoaded', function() {
    const rankingRows = document.querySelectorAll('.ranking-row');
    
    // Animate rows on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, index) => {
            if (entry.isIntersecting) {
                setTimeout(() => {
                    entry.target.style.opacity = '1';
                    entry.target.style.transform = 'translateX(0)';
                }, index * 100);
            }
        });
    }, observerOptions);

    rankingRows.forEach((row, index) => {
        row.style.opacity = '0';
        row.style.transform = 'translateX(-30px)';
        row.style.transition = 'all 0.6s ease';
        observer.observe(row);
    });

    // Add hover effects to stat cards
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.05)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });

    // Animate moyenne bars
    const moyenneBars = document.querySelectorAll('.moyenne-fill');
    moyenneBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0%';
        setTimeout(() => {
            bar.style.transition = 'width 1s ease';
            bar.style.width = width;
        }, 500);
    });

    // Add click effect to ranking rows
    rankingRows.forEach(row => {
        row.addEventListener('click', function() {
            this.style.transform = 'scale(0.98)';
            setTimeout(() => {
                this.style.transform = '';
            }, 200);
        });
    });

    // Highlight top 3 students
    const topThree = document.querySelectorAll('.ranking-row[data-rank="1"], .ranking-row[data-rank="2"], .ranking-row[data-rank="3"]');
    topThree.forEach(row => {
        row.style.boxShadow = '0 8px 30px rgba(255, 215, 0, 0.3)';
        
        // Add glow effect
        setInterval(() => {
            row.style.boxShadow = '0 8px 30px rgba(255, 215, 0, 0.5)';
            setTimeout(() => {
                row.style.boxShadow = '0 8px 30px rgba(255, 215, 0, 0.3)';
            }, 1000);
        }, 2000);
    });

    // Animate stat values
    const statValues = document.querySelectorAll('.stat-value');
    statValues.forEach(stat => {
        const finalValue = stat.textContent;
        const isNumber = !isNaN(parseFloat(finalValue));
        
        if (isNumber) {
            const targetValue = parseFloat(finalValue);
            let currentValue = 0;
            const increment = targetValue / 50;
            const timer = setInterval(() => {
                currentValue += increment;
                if (currentValue >= targetValue) {
                    stat.textContent = finalValue;
                    clearInterval(timer);
                } else {
                    stat.textContent = currentValue.toFixed(2);
                }
            }, 30);
        }
    });

    // Add search functionality if needed
    const searchInput = document.getElementById('searchInput');
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            rankingRows.forEach(row => {
                const text = row.textContent.toLowerCase();
                if (text.includes(searchTerm)) {
                    row.style.display = '';
                    row.style.animation = 'fadeInUp 0.5s ease';
                } else {
                    row.style.display = 'none';
                }
            });
        });
    }

    // Add smooth scroll to top button
    const scrollTopBtn = document.createElement('button');
    scrollTopBtn.innerHTML = '↑';
    scrollTopBtn.className = 'scroll-top-btn';
    scrollTopBtn.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        font-size: 1.5rem;
        cursor: pointer;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.3);
        opacity: 0;
        transition: all 0.3s ease;
        z-index: 1000;
    `;
    
    document.body.appendChild(scrollTopBtn);

    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollTopBtn.style.opacity = '1';
        } else {
            scrollTopBtn.style.opacity = '0';
        }
    });

    scrollTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});








