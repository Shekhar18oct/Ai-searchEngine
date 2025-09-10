document.addEventListener('DOMContentLoaded', function() {
    // Tab elements
    const localSearchTab = document.getElementById('localSearchTab');
    const webSearchTab = document.getElementById('webSearchTab');
    
    // Form elements
    const localSearchForm = document.getElementById('localSearchForm');
    const webSearchForm = document.getElementById('webSearchForm');
    
    // Results elements
    const localSearchResults = document.getElementById('localSearchResults');
    const webSearchResults = document.getElementById('webSearchResults');

    // Tab switching functionality
    localSearchTab.addEventListener('click', () => switchTab('local'));
    webSearchTab.addEventListener('click', () => switchTab('web'));

    function switchTab(tab) {
        // Update tab buttons
        localSearchTab.classList.toggle('active', tab === 'local');
        webSearchTab.classList.toggle('active', tab === 'web');

        // Update forms
        localSearchForm.classList.toggle('active', tab === 'local');
        webSearchForm.classList.toggle('active', tab === 'web');

        // Update results
        localSearchResults.classList.toggle('active', tab === 'local');
        webSearchResults.classList.toggle('active', tab === 'web');
    }

    // Handle local search form submission
    localSearchForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        const query = document.getElementById('localSearchQuery').value;
        
        if (!query) return;

        // Show loading state
        localSearchResults.innerHTML = '<div class="text-center"><div class="loading mx-auto"></div></div>';

        try {
            const response = await fetch(`/search?q=${encodeURIComponent(query)}`);
            const data = await response.json();

            // Display results
            displaySearchResults(data.results);
        } catch (error) {
            showToast('Error performing search', 'error');
        }
    });



    // Function to display local search results
    function displaySearchResults(results) {
        if (!results || results.length === 0) {
            localSearchResults.innerHTML = `
                <div class="text-center text-gray-600 p-8">
                    <p class="mb-4">No local results found</p>
                    <button onclick="switchTab('web')" 
                            class="text-indigo-600 hover:text-indigo-800 underline">
                        Try searching the web →
                    </button>
                </div>
            `;
            return;
        }

        const resultsHTML = results.map(result => `
            <div class="search-result relative bg-white p-6 rounded-lg shadow-md mb-4">
                <div class="similarity-score">${(result.similarity_score * 100).toFixed(1)}% match</div>
                <h3 class="text-xl font-semibold text-gray-800 mb-2">${result.title}</h3>
                <p class="text-gray-600 mb-4">${result.content}</p>
                <div class="flex flex-wrap gap-4">
                    ${result.url ? `
                        <a href="${result.url}" target="_blank" 
                           class="text-indigo-600 hover:text-indigo-800 transition-colors">
                            Learn more →
                        </a>
                    ` : ''}
                    <a href="https://www.google.com/search?q=${encodeURIComponent(result.title)}" 
                       target="_blank"
                       class="text-green-600 hover:text-green-800 transition-colors">
                        Search on Google →
                    </a>
                </div>
            </div>
        `).join('');

        localSearchResults.innerHTML = resultsHTML;
    }

    // Function to show toast notifications
    function showToast(message, type = 'success') {
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.textContent = message;
        document.body.appendChild(toast);

        // Show the toast
        setTimeout(() => toast.classList.add('show'), 100);

        // Remove the toast after 3 seconds
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // Load initial documents
    fetch('/documents')
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                displaySearchResults(data);
            }
        })
        .catch(error => console.error('Error loading documents:', error));
});
