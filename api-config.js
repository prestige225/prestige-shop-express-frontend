// Configuration de l'API
// Forcer l'utilisation du backend Render pour éviter les problèmes de CORS en développement local
const API_BASE_URL = 'https://prestige-shop-backend.onrender.com/api';

// Fonction utilitaire pour effectuer les appels API avec gestion des erreurs
function apiCall(endpoint, options = {}) {
    const url = `${API_BASE_URL}${endpoint}`;
    
    // Ajout des en-têtes par défaut
    const defaultHeaders = {
        'Content-Type': 'application/json',
    };
    
    const config = {
        ...options,
        headers: {
            ...defaultHeaders,
            ...options.headers,
        },
    };
    
    return fetch(url, config)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Erreur API:', error);
            throw error;
        });
}

// Export pour une utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API_BASE_URL, apiCall };
}