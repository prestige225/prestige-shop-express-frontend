/**
 * Fonctions pour afficher les produits recommandés et du moment
 * Intégration dynamique dans index.html
 */

/**
 * Charge et affiche les produits recommandés
 */
async function loadRecommendedProducts() {
    try {
        console.log('📌 Chargement des produits recommandés...');
        
        // Charger tous les produits et filtrer
        const response = await fetch('/api/produits');
        
        if (!response.ok) throw new Error('Erreur API');
        
        const data = await response.json();
        
        if (data.success && data.produits && data.produits.length > 0) {
            // Filtrer les produits recommandés
            const recommandes = data.produits.filter(p => (p.recommande === true || p.recommande === 1) && (p.statut === 'actif' || !p.statut));
            displayRecommendedProducts(recommandes.length > 0 ? recommandes : data.produits.slice(0, 10));
        } else {
            console.log('Aucun produit trouvé');
            const container = document.getElementById('recommended-carousel');
            if (container) container.innerHTML = '<p class="text-gray-500 text-center w-full">Aucun produit disponible</p>';
        }
    } catch (error) {
        console.error('❌ Erreur lors du chargement des produits recommandés:', error);
    }
}

/**
 * Affiche les produits recommandés dans le carousel
 */
function displayRecommendedProducts(products) {
    try {
        const container = document.getElementById('recommended-carousel');
        if (!container) {
            console.warn('Conteneur recommended-carousel non trouvé');
            return;
        }
        
        container.innerHTML = '';
        
        const filtered = products.slice(0, 10);
        
        if (filtered.length === 0) {
            container.innerHTML = '<p class="text-gray-500 text-center w-full py-8">Aucun produit recommandé</p>';
            return;
        }
        
        filtered.forEach(product => {
            const card = createProductCarouselCard(product, 'recommended');
            container.innerHTML += card;
        });
        
        console.log(`✅ ${filtered.length} produits recommandés affichés`);
    } catch (error) {
        console.error('Erreur dans displayRecommendedProducts:', error);
    }
}

/**
 * Charge et affiche les produits du moment
 */
async function loadMomentProducts() {
    try {
        console.log('🔥 Chargement des produits du moment...');
        
        // Charger tous les produits et filtrer
        const response = await fetch('/api/produits');
        
        if (!response.ok) throw new Error('Erreur API');
        
        const data = await response.json();
        
        if (data.success && data.produits && data.produits.length > 0) {
            // Filtrer les produits du moment
            const moments = data.produits.filter(p => (p.moment === true || p.moment === 1) && (p.statut === 'actif' || !p.statut));
            displayMomentProducts(moments.length > 0 ? moments : data.produits.slice(10, 20));
        } else {
            console.log('Aucun produit trouvé');
            const container = document.getElementById('moment-carousel');
            if (container) container.innerHTML = '<p class="text-gray-500 text-center w-full">Aucun produit disponible</p>';
        }
    } catch (error) {
        console.error('❌ Erreur lors du chargement des produits du moment:', error);
    }
}

/**
 * Affiche les produits du moment dans le carousel
 */
function displayMomentProducts(products) {
    try {
        const container = document.getElementById('moment-carousel');
        if (!container) {
            console.warn('Conteneur moment-carousel non trouvé');
            return;
        }
        
        container.innerHTML = '';
        
        const filtered = products.slice(0, 10);
        
        if (filtered.length === 0) {
            container.innerHTML = '<p class="text-gray-500 text-center w-full py-8">Aucun produit du moment</p>';
            return;
        }
        
        filtered.forEach(product => {
            const card = createProductCarouselCard(product, 'moment');
            container.innerHTML += card;
        });
        
        console.log(`✅ ${filtered.length} produits du moment affichés`);
    } catch (error) {
        console.error('Erreur dans displayMomentProducts:', error);
    }
}

/**
 * Crée une carte produit pour le carousel
 */
function createProductCarouselCard(product, type = 'recommended') {
    const image = product.image_url || 'https://via.placeholder.com/250x250?text=Produit';
    const price = product.prix ? product.prix.toLocaleString() : '0';
    const badge = type === 'recommended' 
        ? '<span class="absolute top-2 left-2 bg-yellow-400 text-white px-2 py-1 rounded-full text-xs font-bold flex items-center"><i class="fas fa-star mr-1"></i> Recommandé</span>'
        : '<span class="absolute top-2 left-2 bg-red-500 text-white px-2 py-1 rounded-full text-xs font-bold flex items-center"><i class="fas fa-fire mr-1"></i> Du Moment</span>';
    
    return `
        <div class="flex-shrink-0 w-40 sm:w-48 bg-white rounded-xl shadow-md hover:shadow-xl transition-all overflow-hidden cursor-pointer group" onclick="addToCart({id: ${product.id}, nom: '${(product.nom || '').replace(/'/g, "\\'")}', prix: ${product.prix || 0}, image_url: '${image}'})">
            <div class="relative overflow-hidden h-48 bg-gray-100">
                <img src="${image}" alt="${product.nom || 'Produit'}" class="w-full h-full object-cover group-hover:scale-110 transition-transform duration-300" onerror="this.src='https://via.placeholder.com/250x250?text=Image+non+trouvée'">
                ${badge}
                ${product.stock === 0 ? '<div class="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center"><span class="text-white font-bold">Rupture</span></div>' : ''}
            </div>
            <div class="p-3">
                <h3 class="font-semibold text-sm line-clamp-2 text-gray-800">${product.nom || 'Produit'}</h3>
                <p class="text-purple-600 font-bold text-sm mt-1">${price} FCFA</p>
                <p class="text-gray-500 text-xs mt-1">${product.categorie || 'Sans catégorie'}</p>
                <button class="w-full mt-3 bg-purple-600 hover:bg-purple-700 text-white text-xs font-semibold py-2 px-2 rounded-lg transition-all transform hover:scale-105">
                    <i class="fas fa-shopping-cart mr-1"></i> Ajouter
                </button>
            </div>
        </div>
    `;
}

/**
 * Initialiser le chargement des produits spéciaux au démarrage
 */
function initSpecialProducts() {
    console.log('🚀 Initialisation des produits spéciaux...');
    
    // Attendre que le DOM soit chargé et que les produits soient prêts
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', () => {
            setTimeout(() => {
                loadRecommendedProducts();
                loadMomentProducts();
            }, 1000);
        });
    } else {
        setTimeout(() => {
            loadRecommendedProducts();
            loadMomentProducts();
        }, 1000);
    }
}

// Lancer l'initialisation
try {
    initSpecialProducts();
} catch(e) {
    console.error('Erreur lors de l\'initialisation:', e);
}
