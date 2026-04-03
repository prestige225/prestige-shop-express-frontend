// Configuration de l'API (idempotente pour éviter les reloads multiples)
if (typeof window.API_BASE_URL === 'undefined') {
    // Auto-détection intelligent du backend API
    const hostname = window.location.hostname;
    const protocol = window.location.protocol; // http: ou https:
    
    // En développement local
    if (['localhost', '127.0.0.1'].includes(hostname)) {
        // Utiliser le même hôte et port que la page
        const port = window.location.port;
        window.API_BASE_URL = `${protocol}//${hostname}:${port || (protocol === 'https:' ? 443 : 80)}/api`;
        console.log('🔧 Backend LOCAL activé:', window.API_BASE_URL);
    } else {
        // En production (Render, etc.) - utiliser le même domaine
        window.API_BASE_URL = `${protocol}//${hostname}/api`;
        console.log('🔧 Backend PRODUCTION activé:', window.API_BASE_URL);
    }
    
    // Fallback en cas de problème
    window.API_FALLBACK_URL = window.API_BASE_URL;
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