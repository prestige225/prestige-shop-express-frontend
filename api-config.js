// Configuration de l'API (idempotente pour éviter les reloads multiples)
if (typeof window.API_BASE_URL === 'undefined') {
    // Backend Render fonctionne correctement - toujours l'utiliser
    window.API_BASE_URL = 'https://prestige-shop-backend.onrender.com/api';
    window.API_FALLBACK_URL = 'https://prestige-shop-backend.onrender.com/api';
}

// Fonction utilitaire pour effectuer les appels API avec gestion des erreurs
function apiCall(endpoint, options = {}) {
    const url = `${window.API_BASE_URL}${endpoint}`;
    
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
            // Gérer l'erreur de connexion de manière plus descriptive
            if (error instanceof TypeError && error.message === 'Failed to fetch') {
                throw new Error('Impossible de se connecter au serveur. Vérifiez votre connexion Internet et que le service est bien démarré.');
            }
            throw error;
        });
}

// Export pour une utilisation dans d'autres modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { API_BASE_URL: window.API_BASE_URL, apiCall };
}