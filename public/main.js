document.addEventListener('DOMContentLoaded', () => {
    const emailInput = document.getElementById('email');
    const passwordInput = document.getElementById('password');
    const fetchBtn = document.getElementById('fetch-btn');
    const acceptBtn = document.getElementById('accept-btn');
    const headlineKeywordsInput = document.getElementById('headline-keywords');
    const minMutualInput = document.getElementById('min-mutual');
    const statusDiv = document.getElementById('status');
    const profilesContainer = document.getElementById('profiles-table-container');

    let allProfiles = [];
    let filteredProfiles = [];

    // --- API Communication ---
    async function apiCall(body) {
        try {
            const response = await fetch('/api/linkedin', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(body),
            });
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
            }
            return await response.json();
        } catch (error) {
            console.error('API Call failed:', error);
            updateStatus(`Error: ${error.message}`, 'error');
            return null;
        }
    }

    // --- UI Updates ---
    function updateStatus(message, type = 'info') {
        statusDiv.textContent = message;
        statusDiv.style.color = type === 'error' ? 'red' : 'green';
    }

    function toggleLoading(isLoading) {
        fetchBtn.disabled = isLoading;
        acceptBtn.disabled = isLoading;
        fetchBtn.textContent = isLoading ? 'Fetching...' : 'Fetch Pending Requests';
        acceptBtn.textContent = isLoading ? 'Accepting...' : 'Accept Filtered Connections';
    }

    function renderTable(profiles) {
        if (profiles.length === 0) {
            profilesContainer.innerHTML = '<p>No profiles match the current filters.</p>';
            acceptBtn.style.display = 'none';
            return;
        }

        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Name</th>
                    <th>Headline</th>
                    <th>Mutual Connections</th>
                </tr>
            </thead>
            <tbody>
                ${profiles.map(p => `
                    <tr>
                        <td><a href="${p.profile_url}" target="_blank">${p.name}</a></td>
                        <td>${p.headline}</td>
                        <td>${p.mutual_connections}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;
        profilesContainer.innerHTML = '';
        profilesContainer.appendChild(table);
        acceptBtn.style.display = 'block';
    }

    // --- Event Handlers ---
    async function handleFetch() {
        const email = emailInput.value;
        const password = passwordInput.value;

        if (!email || !password) {
            updateStatus('Please enter your LinkedIn credentials.', 'error');
            return;
        }

        toggleLoading(true);
        updateStatus('Logging in and fetching requests...', 'info');
        
        const data = await apiCall({ action: 'fetch', email, password });

        toggleLoading(false);
        if (data && data.profiles) {
            allProfiles = data.profiles;
            updateStatus(`Successfully fetched ${data.count} pending requests.`, 'success');
            applyFilters();
        }
    }

    async function handleAccept() {
        const email = emailInput.value;
        const password = passwordInput.value;
        const headlineKeywords = headlineKeywordsInput.value.split(',').map(kw => kw.trim()).filter(kw => kw);
        const minMutual = parseInt(minMutualInput.value, 10) || 0;

        toggleLoading(true);
        updateStatus('Accepting filtered connection requests...', 'info');

        const data = await apiCall({
            action: 'accept',
            email,
            password,
            headline_keywords: headlineKeywords,
            min_mutual: minMutual,
        });

        toggleLoading(false);
        if (data) {
            updateStatus(data.message || `Accepted ${data.accepted_count} connections.`, 'success');
            // Re-fetch to show the updated list of pending requests
            handleFetch();
        }
    }
    
    function applyFilters() {
        const headlineKeywords = headlineKeywordsInput.value.split(',').map(kw => kw.trim().toLowerCase()).filter(kw => kw);
        const minMutual = parseInt(minMutualInput.value, 10) || 0;

        filteredProfiles = allProfiles.filter(p => {
            const headline = p.headline.toLowerCase();
            const mutualCount = parseInt(p.mutual_connections.match(/\d+/) || ['0'][0], 10);
            
            const keywordMatch = headlineKeywords.length === 0 || headlineKeywords.some(kw => headline.includes(kw));
            const mutualMatch = mutualCount >= minMutual;

            return keywordMatch && mutualMatch;
        });
        
        updateStatus(`Showing ${filteredProfiles.length} of ${allProfiles.length} profiles.`, 'info');
        renderTable(filteredProfiles);
    }

    // --- Attach Event Listeners ---
    fetchBtn.addEventListener('click', handleFetch);
    acceptBtn.addEventListener('click', handleAccept);
    headlineKeywordsInput.addEventListener('input', applyFilters);
    minMutualInput.addEventListener('input', applyFilters);
}); 