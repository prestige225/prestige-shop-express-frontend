# Analyse du Chargement des Produits par Catégorie - index.html

## 📊 Résumé des Trouvailles

- **Limite d'affichage:** 8 produits par page
- **API Call:** Récupère 500 produits avec `limit=500&offset=0`
- **Filtrage:** Effectué en JavaScript côté client
- **Articles similaires:** TOUS les produits de la même catégorie (pas de limite)

---

## 1️⃣ Variable de Configuration - Limite 8 articles

**Ligne 5425:**
```javascript
let productsPerPage = 8; // Nombre de produits par page
```

---

## 2️⃣ API Call pour Charger les Produits

**Ligne 5820 (dans `loadProducts()`):**
```javascript
// ⚡ 2️⃣ CHARGER DEPUIS L'API (toujours, pour synchro)
console.log('⚡ Synchronisation avec l\'API...');
let response = await fetch(`${window.API_BASE_URL}/produits?limit=500&offset=0`);

// Si localhost ne fonctionne pas, fallback vers le backend Render
if (!response.ok && window.API_BASE_URL.includes('localhost') && window.API_FALLBACK_URL) {
    console.warn('⚠️ API locale indisponible, basculement vers le backend Render...');
    response = await fetch(`${window.API_FALLBACK_URL}/produits?limit=500&offset=0`);
}

if (!response.ok) {
    throw new Error(`Erreur HTTP: ${response.status}`);
}

const data = await response.json();

if (data.success && data.produits && Array.isArray(data.produits)) {
    console.log(`📡 API: ${data.produits.length} produits récupérés`);
    
    // Mapper les produits
    const apiProducts = data.produits.map(p => mapApiProductToFrontend(p));
    
    // 💾 REMPLACER AVEC les données fraîches de l'API
    allProducts = apiProducts;
    loadedProductIds.clear();
    allProducts.forEach(p => loadedProductIds.add(String(p.id).trim()));
    
    // Trier
    allProducts.sort((a, b) => a.ordre - b.ordre);
    
    // Afficher
    currentPage = 1;
    displayProducts(currentFilter, true);
    console.log(`✅ ${allProducts.length} produits affichés (synchronisés avec API)`);
}
```

---

## 3️⃣ Normalisation des Catégories - mapApiProductToFrontend()

**Ligne 5480:**
```javascript
function mapApiProductToFrontend(apiProduct) {
    // ... (gestion des images et vidéos)
    
    return {
        id: apiProduct.id,
        name: apiProduct.nom,
        price: apiProduct.prix,
        originalPrice: originalPrice,
        discountPercent: 20,
        // ✅ NORMALISATION: "💼 Prestige Business" -> "business"
        category: apiProduct.categorie === '💼 Prestige Business' ? 'business' : 
                  apiProduct.categorie === '💼 Business' ? 'business' : 
                  apiProduct.categorie || '',
        subcategory: apiProduct.subcategorie || apiProduct.sous_categorie || '',
        images: mediaArray,
        videos: videos,
        description: apiProduct.description || '',
        sizes: Array.isArray(apiProduct.taille_disponible) ? apiProduct.taille_disponible : 
                (typeof apiProduct.taille_disponible === 'string' ? JSON.parse(apiProduct.taille_disponible || '[]') : []),
        colors: Array.isArray(apiProduct.couleur_disponible) ? apiProduct.couleur_disponible : 
                (typeof apiProduct.couleur_disponible === 'string' ? JSON.parse(apiProduct.couleur_disponible || '[]') : []),
        stock: apiProduct.stock || 0,
        status: apiProduct.statut || 'actif',  // ✅ Statut: actif, inactif, epuise
        ordre: apiProduct.ordre || 9999,
        quantiteMinimale: apiProduct.quantite_minimale || 1,
        recommande: apiProduct.recommande || 0,  // ✅ Produit recommandé
        moment: apiProduct.moment || 0  // ✅ Produit du moment
    };
}
```

---

## 4️⃣ Filtrage par Catégorie - filterProducts()

**Ligne 6655:**
```javascript
// Filtrage des produits
function filterProducts(category) {
    currentFilter = category;
    currentPage = 1; // Reset à la première page
    
    // Si l'utilisateur demande "Tous les produits" et que le chargement initial n'est pas fini,
    // lancer immédiatement le chargement du reste
    if (category === 'all' && !isInitialLoadComplete && !isLoadingRemainingProducts) {
        console.log('📌 Chargement urgent des produits restants...');
        loadRemainingProducts();
    }
    
    displayProducts(category, true);
    
    // Mise à jour des tags de catégories actifs
    document.querySelectorAll('.category-tag').forEach(tag => {
        tag.classList.remove('ring-2', 'ring-white', 'ring-opacity-50');
    });
    
    // Gestion des sous-catégories et catégories
    if (category.startsWith('mode-')) {
        // Pour les sous-catégories mode, activer le tag Mode
        const tags = document.querySelectorAll('.category-tag');
        tags[3]?.classList.add('ring-2', 'ring-white', 'ring-opacity-50');
    } else if (category === 'mode') {
        // ... autres catégories
    } else if (category === 'business') {
        // Activer le tag Business
        const tags = document.querySelectorAll('.category-tag');
        tags[6]?.classList.add('ring-2', 'ring-white', 'ring-opacity-50');
    }
    
    // Gestion des descriptions de catégories
    document.querySelectorAll('.category-description').forEach(desc => {
        desc.classList.add('hidden');
    });
    
    // Faire défiler vers les produits
    setTimeout(() => {
        document.getElementById('produits').scrollIntoView({ 
            behavior: 'smooth',
            block: 'start'
        });
    }, 100);
}
```

---

## 5️⃣ Affichage et Pagination - displayProducts()

**Ligne 6326:**
```javascript
// Affichage des produits
function displayProducts(filter = 'all', reset = true) {
    if (reset) {
        currentPage = 1;
        currentFilter = filter;
    }
    
    const grid = document.getElementById('products-grid');
    let filteredProducts;
    
    // Gérer les sous-catégories mode
    if (filter.startsWith('mode-')) {
        const subcategory = filter.replace('mode-', '');
        filteredProducts = allProducts.filter(p => 
            p.category === 'mode' && 
            (p.subcategory?.toLowerCase() === subcategory.toLowerCase() || 
             p.subcategory?.toLowerCase().includes(subcategory.toLowerCase()))
        );
    } else if (filter === 'all') {
        filteredProducts = allProducts;
    } else if (filter === 'mode') {
        filteredProducts = allProducts.filter(p => p.category === 'mode');
    } else {
        // ✅ FILTRAGE PAR CATÉGORIE PRINCIPALE (ex: 'business', 'electronique', etc.)
        filteredProducts = allProducts.filter(p => p.category === filter);
    }
    
    // Déduplique les produits filtrés
    filteredProducts = removeDuplicateProducts(filteredProducts);
    filteredProducts = sortProductsArray(filteredProducts, currentSort);
    
    // ✅ LIMITATION À 8 PRODUITS PAR PAGE
    const endIndex = currentPage * productsPerPage;  // currentPage * 8
    const productsToShow = filteredProducts.slice(0, endIndex);
    
    if (reset) grid.innerHTML = '';
    
    const newProductsHTML = productsToShow
        .slice(reset ? 0 : (currentPage - 1) * productsPerPage)
        .map(product => createProductCard(product))
        .join('');
    
    if (reset) grid.innerHTML = newProductsHTML;
    else grid.insertAdjacentHTML('beforeend', newProductsHTML);
    
    // Initialiser les carousels des produits
    const newProducts = reset 
        ? productsToShow 
        : productsToShow.slice((currentPage - 1) * productsPerPage);
    
    newProducts.forEach(product => {
        initializeCarousel(product.id);
    });
    
    // Marquer les favoris dans l'interface
    markFavoritesInUI();
    
    // Afficher les produits recommandés
    displayRecommendedProducts();
}
```

---

## 6️⃣ Chargement avec Pagination au Scroll - loadMoreProducts()

**Ligne 6544:**
```javascript
// Charger plus de produits avec animation rapide
function loadMoreProducts() {
    // ✅ NE RIEN FAIRE SI ON EST SUR LA CATÉGORIE BUSINESS
    if (currentFilter === 'business') return;
    
    if (isLoadingMore) return;
    
    // Si le chargement initial n'est pas fini mais que nous avons assez de produits pour paginer, continuer
    if (!isInitialLoadComplete && allProducts.length < productsPerPage * 2) {
        // Lancer le chargement du reste si pas déjà en cours
        if (!isLoadingRemainingProducts) {
            loadRemainingProducts();
        }
        return;
    }
    
    let filteredProducts;
    // Filtrer les produits selon le filtre courant
    if (currentFilter.startsWith('mode-')) {
        const subcategory = currentFilter.replace('mode-', '');
        filteredProducts = allProducts.filter(p => 
            p.category === 'mode' && 
            (p.subcategory?.toLowerCase() === subcategory.toLowerCase() || 
             p.subcategory?.toLowerCase().includes(subcategory.toLowerCase()))
        );
    } else if (currentFilter === 'all') {
        filteredProducts = allProducts;
    } else if (currentFilter === 'mode') {
        filteredProducts = allProducts.filter(p => p.category === 'mode');
    } else {
        filteredProducts = allProducts.filter(p => p.category === currentFilter);
    }
    
    // ✅ VÉRIFIER SI ON A PLUS DE PRODUITS À AFFICHER
    if (currentPage * productsPerPage >= filteredProducts.length) return;
    
    isLoadingMore = true;
    currentPage++;  // Incrémenter la page
    displayProducts(currentFilter, false);
    
    // Animation des nouvelles cartes
    const newCards = document.querySelectorAll('.product-card');
    const startIndex = (currentPage - 1) * productsPerPage;
    
    for (let i = startIndex; i < newCards.length; i++) {
        if (newCards[i]) {
            newCards[i].style.opacity = '0';
            newCards[i].style.transform = 'translateY(20px)';
            
            setTimeout(() => {
                newCards[i].style.transition = 'all 0.4s ease';
                newCards[i].style.opacity = '1';
                newCards[i].style.transform = 'translateY(0)';
            }, (i - startIndex) * 80);
        }
    }
    
    isLoadingMore = false;
}
```

---

## 7️⃣ Articles Similaires - openProductQuickView()

**Ligne 9268 (dans `openProductQuickView()`):**
```javascript
// Trouver produits similaires - afficher TOUS les produits de la même catégorie
const similarProducts = allProducts.filter(p => 
    p.category === product.category && p.id !== product.id
);

// ✅ AFFICHAGE DE TOUS LES PRODUITS SIMILAIRES (PAS DE LIMITE DE 8)
// Les articles similaires sont affichés dans un carousel horizontal
const carouselHTML = similarProducts.map(p => {
    const isSimilarOutOfStock = p.status === 'epuise';
    return `
        <div class="flex-shrink-0 w-40 group ${isSimilarOutOfStock ? 'opacity-60 grayscale' : ''}">
            <div class="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-all 
                    ${isSimilarOutOfStock ? 'cursor-not-allowed' : 'cursor-pointer'} border border-gray-100 h-full flex flex-col" 
                    ${!isSimilarOutOfStock ? `onclick="openProductQuickView(${p.id})"` : ''}>
                <div class="relative w-full h-40 overflow-hidden bg-gray-100">
                    <img src="${getAbsoluteImagePath(getProductMainImage(p))}" 
                         alt="${p.name}" 
                         class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300 p-2"
                         onerror="this.src='/images/placeholder.png';">
                    
                    ${isSimilarOutOfStock ? `
                    <!-- Badge Rupture de Stock -->
                    <div class="absolute top-2 right-2 bg-red-600 text-white px-2 py-1 rounded-full text-xs font-bold shadow-lg">
                        <i class="fas fa-ban"></i>
                    </div>
                    ` : `
                    <!-- Like/Favorite Button -->
                    <button onclick="event.stopPropagation(); toggleFavorite(${p.id}, this);" 
                            class="absolute top-2 right-2 bg-white/90 hover:bg-white text-red-500 hover:text-red-600 p-2 rounded-full shadow-md hover:shadow-lg transition-all z-10 active:scale-90">
                        <i class="fas fa-heart text-lg"></i>
                    </button>
                    
                    <!-- Badge Discount -->
                    <div class="absolute bottom-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-xs shadow-lg">
                        -${p.discountPercent || 20}%
                    </div>
                    `}
                </div>
                <div class="p-3 flex-1 flex flex-col">
                    <h4 class="font-bold text-sm text-gray-800 line-clamp-2 mb-1">${p.name}</h4>
                    <p class="text-xs text-gray-500 mb-2">${getCategoryName(p.category)}</p>
                    <div class="mt-auto mb-2">
                        <span class="font-bold ${isSimilarOutOfStock ? 'text-gray-500' : 'text-purple-600'}">${p.price.toLocaleString()} FCFA</span>
                    </div>
                    ${isSimilarOutOfStock ? `
                    <button disabled class="w-full h-8 bg-gray-300 text-gray-500 rounded-lg font-bold text-xs cursor-not-allowed flex items-center justify-center">
                        <i class="fas fa-ban text-xs mr-0.5"></i> Indisponible
                    </button>
                    ` : `
                    <button onclick="event.stopPropagation(); addToCart(${p.id})" 
                            class="w-full h-8 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-bold text-xs transition-all flex items-center justify-center">
                        <i class="fas fa-plus text-xs mr-0.5"></i> Ajouter
                    </button>
                    `}
                </div>
            </div>
        </div>
    `;
}).join('');
```

---

## 8️⃣ Produits Recommandés - displayRecommendedProducts()

**Ligne 7237:**
```javascript
// Afficher les produits recommandés dans le panier
function displayRecommendedProducts() {
    const recommendedCarousels = document.querySelectorAll('#recommended-carousel');
    if (recommendedCarousels.length === 0) return;

    // ✅ FILTRER LES PRODUITS AVEC recommande = 1
    const recommendedProducts = allProducts.filter(product => {
        return (product.recommande === 1 || product.recommande === '1')
               && product.status !== 'epuise';  // EXCLURE les produits épuisés
    });

    // Générer le HTML pour chaque produit (SANS LIMITE)
    const carouselHTML = recommendedProducts.map(product => {
        const imageUrl = getProductMainImage(product);
        const discount = product.discountPercent || 20;
        
        return `
            <div class="flex-shrink-0 w-40 group">
                <div class="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-lg transition-all cursor-pointer border border-gray-100 h-full flex flex-col">
                    <!-- Image -->
                    <div class="relative w-full h-40 overflow-hidden bg-gray-100 cursor-pointer" onclick="openProductQuickView(${product.id})">
                        <img src="${getAbsoluteImagePath(imageUrl)}" 
                             alt="${product.name}" 
                             class="w-full h-full object-contain group-hover:scale-105 transition-transform duration-300 p-2"
                             onerror="this.src='/images/placeholder.png';">
                        
                        <!-- Like/Favorite Button -->
                        <button onclick="event.stopPropagation(); toggleFavorite(${product.id}, this);" 
                                class="absolute top-2 right-12 bg-white/90 hover:bg-white text-red-500 hover:text-red-600 p-2 rounded-full shadow-md hover:shadow-lg transition-all z-10 active:scale-90">
                            <i class="fas fa-heart text-lg"></i>
                        </button>
                        
                        <!-- Badge discount -->
                        <div class="absolute bottom-2 right-2 bg-red-500 text-white rounded-full w-8 h-8 flex items-center justify-center font-bold text-xs shadow-lg">
                            -${discount}%
                        </div>
                    </div>

                    <!-- Contenu -->
                    <div class="p-3 flex-1 flex flex-col">
                        <h4 class="font-bold text-sm text-gray-800 line-clamp-2 mb-1">${product.name}</h4>
                        <p class="text-xs text-gray-500 mb-2">${product.category || 'Produit'}</p>
                        
                        <div class="mt-auto mb-2">
                            <span class="font-bold text-purple-600">${product.price.toLocaleString()} FCFA</span>
                        </div>

                        <button onclick="addQuickToCart(${product.id}, '...')" 
                                class="w-full h-8 bg-purple-600 hover:bg-purple-700 text-white rounded-lg font-bold text-xs transition-all">
                            <i class="fas fa-plus text-xs mr-0.5"></i> Ajouter
                        </button>
                    </div>
                </div>
            </div>
        `;
    }).join('');
    
    // Mettre à jour TOUS les carousels recommandés (SANS LIMITE de 8)
    recommendedCarousels.forEach(carousel => {
        carousel.innerHTML = carouselHTML;
    });
    
    markFavoritesInUI();
}
```

---

## 📋 Résumé Comparatif

| Aspect | Catégorie | Articles Similaires | Recommandés |
|--------|-----------|-------------------|-------------|
| **API Call** | `limit=500&offset=0` | Filtre en JS | Filtre en JS |
| **Limite d'affichage** | 8 produits/page | **TOUS** (pas de limite) | **TOUS** (pas de limite) |
| **Filtre appliqué** | `category === filter` | `category === product.category` | `recommande === 1` |
| **Pagination** | Oui (au scroll) | Non (carousel horizontal) | Non (carousel horizontal) |
| **Exclusion épuisés** | Non | Oui (status !== 'epuise') | Oui (status !== 'epuise') |
| **Tri** | Oui (sortProductsArray) | Non | Non |

---

## 🎯 Points Clés

1. **Limite 8:** Uniquement pour l'affichage principal par catégorie
2. **API:** Charge une seule fois avec `limit=500` (pas d'appels multiplespar catégorie)
3. **Business:** Pas de pagination supplémentaire sur `loadMoreProducts()`
4. **Similaires:** Affiche TOUS les produits de la même catégorie en carousel
5. **Recommandés:** Affiche TOUS les produits avec `recommande=1`
