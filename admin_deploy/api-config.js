// Configuration de l'API (idempotente pour éviter les reloads multiples)
if (typeof window.API_BASE_URL === 'undefined') {
    window.API_BASE_URL = window.location.hostname.includes('render.com') || window.location.hostname.includes('onrender')
        ? 'https://prestige-shop-backend.onrender.com/api'
        : 'http://localhost:5000/api';
}

if (typeof window.apiCall === 'undefined') {
    window.apiCall = function apiCall(endpoint, options = {}) {
        const url = `${window.API_BASE_URL}${endpoint}`;
        const defaultHeaders = { 'Content-Type': 'application/json' };
        const config = { ...options, headers: { ...defaultHeaders, ...options.headers } };
        return fetch(url, config)
            .then(response => {
                if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
                return response.json();
            })
            .catch(error => {
                console.error('Erreur API:', error);
                if (error instanceof TypeError && error.message === 'Failed to fetch') {
                    throw new Error('Impossible de se connecter au serveur. Vérifiez votre connexion Internet et que le service est bien démarré.');
                }
                throw error;
            });
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API_BASE_URL: window.API_BASE_URL, apiCall: window.apiCall };
}