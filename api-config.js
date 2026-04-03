// Configuration de l'API (idempotente pour éviter les reloads multiples)
if (typeof window.API_BASE_URL === 'undefined') {
    // Auto-détection intelligent du backend API
    const hostname = window.location.hostname;
    const fullUrl = window.location.href;
    const protocol = window.location.protocol; // http: ou https:
    
    console.log('🔍 API Config - Hostname:', hostname);
    console.log('🔍 API Config - Full URL:', fullUrl);
    
    // En développement local
    if (['localhost', '127.0.0.1'].includes(hostname)) {
        // Ports de backend connus (en priorité)
        const backendPorts = ['5000', '5500', '5504', '5505', '5506'];
        const port = window.location.port;
        
        // Si le port actuel est connu, essayer d'utiliser le backend sur ce port
        if(backendPorts.includes(port)){
            window.API_BASE_URL = `${protocol}//${hostname}:${port}/api`;
            console.log('✅ API détecté sur le port actuel:', window.API_BASE_URL);
        } else {
            // Sinon, essayer le port 5000 par défaut
            window.API_BASE_URL = 'http://localhost:5000/api';
            console.log('⚠️  Fallback vers port 5000:', window.API_BASE_URL);
        }
    } else if (fullUrl.includes('prestige-shop-express.onrender.com')) {
        // Sur Render frontend - utiliser toujours le backend séparé
        window.API_BASE_URL = 'https://prestige-shop-backend.onrender.com/api';
        console.log('🔧 RENDER FRONTEND détecté - Backend séparé activé:', window.API_BASE_URL);
    } else if (fullUrl.includes('prestige-shop-backend.onrender.com')) {
        // Sur Render backend lui-même
        window.API_BASE_URL = 'https://prestige-shop-backend.onrender.com/api';
        console.log('🔧 RENDER BACKEND détecté - API locale:', window.API_BASE_URL);
    } else if (protocol === 'https:') {
        // En HTTPS production - utiliser prestige-shop-backend en dur
        window.API_BASE_URL = 'https://prestige-shop-backend.onrender.com/api';
        console.log('🔧 HTTPS détecté - Backend Render activé:', window.API_BASE_URL);
    } else {
        // Fallback : construire depuis le domaine actuel
        window.API_BASE_URL = `${protocol}//${hostname}/api`;
        console.log('🔧 Fallback domaine - Backend local activé:', window.API_BASE_URL);
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