/**
 * ScholarSphere - Research Paper Search Engine
 * JavaScript Module for Dynamic Search and Results Display
 */

// Particle Animation Background
class ParticleSystem {
    constructor(canvas) {
        this.canvas = canvas;
        this.ctx = canvas.getContext('2d');
        this.particles = [];
        this.particleCount = 50;
        
        this.resize();
        this.createParticles();
        this.animate();
        
        window.addEventListener('resize', () => this.resize());
    }
    
    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
    }
    
    createParticles() {
        for (let i = 0; i < this.particleCount; i++) {
            this.particles.push({
                x: Math.random() * this.canvas.width,
                y: Math.random() * this.canvas.height,
                vx: (Math.random() - 0.5) * 0.5,
                vy: (Math.random() - 0.5) * 0.5,
                radius: Math.random() * 2 + 1,
                opacity: Math.random() * 0.5 + 0.2
            });
        }
    }
    
    animate() {
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        this.particles.forEach(particle => {
            // Update position
            particle.x += particle.vx;
            particle.y += particle.vy;
            
            // Wrap around edges
            if (particle.x < 0) particle.x = this.canvas.width;
            if (particle.x > this.canvas.width) particle.x = 0;
            if (particle.y < 0) particle.y = this.canvas.height;
            if (particle.y > this.canvas.height) particle.y = 0;
            
            // Draw particle
            this.ctx.beginPath();
            this.ctx.arc(particle.x, particle.y, particle.radius, 0, Math.PI * 2);
            this.ctx.fillStyle = `rgba(255, 255, 255, ${particle.opacity})`;
            this.ctx.fill();
        });
        
        // Draw connections
        this.particles.forEach((p1, i) => {
            this.particles.slice(i + 1).forEach(p2 => {
                const dx = p1.x - p2.x;
                const dy = p1.y - p2.y;
                const distance = Math.sqrt(dx * dx + dy * dy);
                
                if (distance < 150) {
                    this.ctx.beginPath();
                    this.ctx.strokeStyle = `rgba(255, 255, 255, ${0.1 * (1 - distance / 150)})`;
                    this.ctx.lineWidth = 1;
                    this.ctx.moveTo(p1.x, p1.y);
                    this.ctx.lineTo(p2.x, p2.y);
                    this.ctx.stroke();
                }
            });
        });
        
        requestAnimationFrame(() => this.animate());
    }
}

// Initialize particle system
document.addEventListener('DOMContentLoaded', () => {
    const canvas = document.getElementById('particles');
    if (canvas) {
        new ParticleSystem(canvas);
    }
    
    initializeSearchFunctionality();
});

// Search Functionality
function initializeSearchFunctionality() {
    const form = document.getElementById('researchSearchForm');
    const queryInput = document.getElementById('researchQuery');
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const resultsGrid = document.getElementById('resultsGrid');
    const noResults = document.getElementById('noResults');
    
    // Form submission
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        const query = queryInput.value.trim();
        
        if (!query) return;
        
        await performSearch(query);
    });
    
    // Handle chip selection for visual feedback
    const chips = document.querySelectorAll('.chip');
    chips.forEach(chip => {
        chip.addEventListener('click', () => {
            chips.forEach(c => c.classList.remove('chip-active'));
            chip.classList.add('chip-active');
        });
    });
}

// Quick search function
function quickSearch(query) {
    const input = document.getElementById('researchQuery');
    input.value = query;
    document.getElementById('researchSearchForm').dispatchEvent(new Event('submit'));
}

// Perform research paper search
async function performSearch(query) {
    const loadingSpinner = document.getElementById('loadingSpinner');
    const resultsSection = document.getElementById('resultsSection');
    const resultsGrid = document.getElementById('resultsGrid');
    const noResults = document.getElementById('noResults');
    const searchedQuery = document.getElementById('searchedQuery');
    const resultsCount = document.getElementById('resultsCount');
    
    // Get selected source
    const sourceRadios = document.querySelectorAll('input[name="source"]');
    let source = 'all';
    sourceRadios.forEach(radio => {
        if (radio.checked) source = radio.value;
    });
    
    // Get max results
    const maxResults = document.getElementById('maxResults').value;
    
    // Show loading
    loadingSpinner.style.display = 'block';
    resultsSection.style.display = 'none';
    
    // Scroll to loading spinner
    loadingSpinner.scrollIntoView({ behavior: 'smooth', block: 'center' });
    
    try {
        const response = await fetch(`/research/search?q=${encodeURIComponent(query)}&source=${source}&max=${maxResults}`);
        
        if (!response.ok) {
            throw new Error('Search failed');
        }
        
        const data = await response.json();
        
        // Hide loading
        loadingSpinner.style.display = 'none';
        
        // Update query display
        searchedQuery.textContent = query;
        
        // Display results
        if (source === 'all' && data.results) {
            displayAllResults(data.results, data.results_by_source);
            resultsCount.textContent = data.total_results || data.results.length;
        } else if (data.results) {
            displayAllResults(data.results);
            resultsCount.textContent = data.total_results || data.results.length;
        } else {
            showNoResults();
        }
        
        // Show results section
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
        
    } catch (error) {
        console.error('Search error:', error);
        loadingSpinner.style.display = 'none';
        alert('An error occurred while searching. Please try again.');
    }
}

// Display all search results
function displayAllResults(results, resultsBySource = {}) {
    const resultsGrid = document.getElementById('resultsGrid');
    const noResults = document.getElementById('noResults');
    
    // Update source counts
    if (resultsBySource) {
        document.getElementById('scholarCount').textContent = resultsBySource.scholar || 0;
        document.getElementById('researchgateCount').textContent = resultsBySource.researchgate || 0;
        document.getElementById('wikipediaCount').textContent = resultsBySource.wikipedia || 0;
    }
    
    if (!results || results.length === 0) {
        showNoResults();
        return;
    }
    
    noResults.style.display = 'none';
    resultsGrid.innerHTML = '';
    
    results.forEach((paper, index) => {
        const paperCard = createPaperCard(paper, index);
        resultsGrid.appendChild(paperCard);
    });
}

// Create paper card element
function createPaperCard(paper, index) {
    const card = document.createElement('div');
    card.className = 'paper-card';
    card.style.animationDelay = `${index * 0.05}s`;
    
    // Determine source class
    let sourceClass = 'source-scholar';
    let sourceIcon = 'fa-book';
    if (paper.source === 'ResearchGate') {
        sourceClass = 'source-researchgate';
        sourceIcon = 'fa-flask';
    } else if (paper.source === 'Wikipedia') {
        sourceClass = 'source-wikipedia';
        sourceIcon = 'fab fa-wikipedia-w';
    }
    
    // Format authors
    const authorsText = Array.isArray(paper.authors) 
        ? (paper.authors.length > 3 
            ? paper.authors.slice(0, 3).join(', ') + ' et al.'
            : paper.authors.join(', '))
        : (paper.authors || 'Unknown');
    
    // Build HTML
    card.innerHTML = `
        <div class="paper-header">
            <span class="paper-source-badge ${sourceClass}">
                <i class="fas ${sourceIcon}"></i>
                ${paper.source || 'Unknown'}
            </span>
        </div>
        
        <h3 class="paper-title">${escapeHtml(paper.title)}</h3>
        
        <p class="paper-authors">
            <i class="fas fa-user-graduate"></i> ${escapeHtml(authorsText)}
        </p>
        
        <div class="paper-meta">
            ${paper.year !== 'N/A' ? `
                <div class="meta-item">
                    <i class="far fa-calendar"></i>
                    ${paper.year}
                </div>
            ` : ''}
            ${paper.venue && paper.venue !== 'N/A' ? `
                <div class="meta-item">
                    <i class="fas fa-building"></i>
                    ${escapeHtml(paper.venue)}
                </div>
            ` : ''}
        </div>
        
        <p class="paper-abstract">${escapeHtml(paper.abstract || 'No abstract available')}</p>
        
        <div class="paper-footer">
            ${typeof paper.citations === 'number' ? `
                <div class="citation-count">
                    <i class="fas fa-quote-right"></i>
                    ${paper.citations} citations
                </div>
            ` : '<div></div>'}
            
            ${paper.url ? `
                <a href="${escapeHtml(paper.url)}" target="_blank" class="view-paper-btn" rel="noopener noreferrer">
                    View Paper
                    <i class="fas fa-external-link-alt"></i>
                </a>
            ` : `
                <button class="view-paper-btn" disabled style="opacity: 0.5; cursor: not-allowed;">
                    No Link Available
                </button>
            `}
        </div>
    `;
    
    return card;
}

// Show no results message
function showNoResults() {
    const resultsGrid = document.getElementById('resultsGrid');
    const noResults = document.getElementById('noResults');
    const resultsCount = document.getElementById('resultsCount');
    
    resultsGrid.innerHTML = '';
    noResults.style.display = 'block';
    resultsCount.textContent = '0';
    
    document.getElementById('scholarCount').textContent = '0';
    document.getElementById('researchgateCount').textContent = '0';
    document.getElementById('wikipediaCount').textContent = '0';
}

// Utility function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Add smooth scrolling for all links
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
        e.preventDefault();
        const target = document.querySelector(this.getAttribute('href'));
        if (target) {
            target.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    });
});

// Add fade-in animation on scroll
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Observe feature cards for animation
setTimeout(() => {
    document.querySelectorAll('.feature-card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        card.style.transition = 'all 0.6s ease';
        observer.observe(card);
    });
}, 100);

/**
 * Filter search by source from badge buttons
 */
function filterBySource(source) {
    // Select the appropriate radio button
    const sourceRadio = document.getElementById(`source-${source}`);
    if (sourceRadio) {
        sourceRadio.checked = true;
        
        // Update chip visual state
        document.querySelectorAll('.chip').forEach(chip => {
            chip.classList.remove('chip-active');
        });
        document.querySelector(`label[for="source-${source}"]`).classList.add('chip-active');
        
        // Add visual feedback to badge
        document.querySelectorAll('.clickable-badge').forEach(badge => {
            badge.style.transform = 'scale(1)';
            badge.style.opacity = '0.8';
        });
        
        const clickedBadge = event.target.closest('.clickable-badge');
        if (clickedBadge) {
            clickedBadge.style.transform = 'scale(1.05)';
            clickedBadge.style.opacity = '1';
            
            setTimeout(() => {
                clickedBadge.style.transform = 'scale(1)';
            }, 200);
        }
        
        // Scroll to search section
        document.querySelector('.search-section').scrollIntoView({ 
            behavior: 'smooth', 
            block: 'center' 
        });
        
        // Focus on search input
        setTimeout(() => {
            document.getElementById('researchQuery').focus();
        }, 500);
    }
}

