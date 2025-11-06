// Configuration de l'API
const API_BASE_URL = 'https://prestige-shop-backend.onrender.com/api';

// Fonction utilitaire pour effectuer les appels API
function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    return fetch(url, options);
}

// Export pour une utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API_BASE_URL, apiCall };
}