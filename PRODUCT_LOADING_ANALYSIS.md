# Product Loading Architecture - Prestige Shop Express

## Summary
Products are loaded primarily via API with intelligent caching. There is **NO existing deep linking or URL parameter handling** for product sharing.

---

## 1. **Where Products Array is Defined & Populated**

### Main Array Declaration
**File:** `index.html` - **Line 5044**

```javascript
let allProducts = [];                          // Stockage de tous les produits récupérés de l'API
let loadedProductIds = new Set();              // Tracker des produits déjà chargés
let isLoadingRemainingProducts = false;        // Flag pour éviter les appels multiples
```

### Fallback/Hardcoded Products (Legacy)
**File:** `index.html` - **Line 3757-3850+** (This is fallback data)

```javascript
const products = [
    {
        id: 36,
        name: "Jean Carpenter \"Gothic Cross\"",
        price: 10000,
        category: "mode",
        subcategory: "homme",
        images: [
            "https://imagesend.fr/uploads/20251220/6bbb07c45dbdf0fc23546cfaf0245f129e380f81.jpg",
            ...
        ],
        sizes: ["31", "32", "33", "34"],
        colors: ["Bleu Denim", "Bleu foncé", "Noir"]
    },
    ...
]
```

---

## 2. **How Products Are Loaded (API Integration)**

### Primary Loading Function
**File:** `index.html` - **Lines 5146-5270**

```javascript
async function loadProductsFromApi(forceRefresh = false) {
    // ⚠️ VÉRIFIER SI LE CACHE A CHANGÉ
    const cacheInvalidationFlag = localStorage.getItem('productsCacheInvalidated');
    if (cacheInvalidationFlag === 'true') {
        // Force full reload
    }
    
    try {
        // 📌 1️⃣ AFFICHER LE CACHE DES 8 PREMIERS (instantané!)
        if (!forceRefresh && allProducts.length === 0) {
            const cachedProducts = localStorage.getItem('cachedProducts');
            if (cachedProducts) {
                // Load from cache
                allProducts = JSON.parse(cachedProducts);
                displayProducts(currentFilter, true);
            }
        }
        
        // ⚡ 2️⃣ CHARGER DEPUIS L'API (toujours, pour synchro)
        const response = await fetch(`${window.API_BASE_URL}/produits?limit=500&offset=0`);
        const data = await response.json();
        
        if (data.success && data.produits && Array.isArray(data.produits)) {
            // Map products
            const apiProducts = data.produits.map(p => mapApiProductToFrontend(p));
            
            // Replace with fresh data
            allProducts = apiProducts;
            
            // Sort by order
            allProducts.sort((a, b) => a.ordre - b.ordre);
            
            // Display and cache
            displayProducts(currentFilter, true);
            localStorage.setItem('cachedProducts', JSON.stringify(allProducts));
        }
    } catch (error) {
        console.error('⚠️ Erreur chargement:', error);
    }
}
```

### Data Mapping Function
**File:** `index.html` - **Lines 5086-5140** (mapApiProductToFrontend)

```javascript
function mapApiProductToFrontend(apiProduct) {
    // Handle images (multiple images per product)
    let images = [];
    if (apiProduct.images_urls) {
        images = Array.isArray(apiProduct.images_urls) 
            ? apiProduct.images_urls 
            : JSON.parse(apiProduct.images_urls);
    }
    
    // Handle videos
    let videos = [];
    if (apiProduct.videos_urls) {
        videos = Array.isArray(apiProduct.videos_urls)
            ? apiProduct.videos_urls
            : JSON.parse(apiProduct.videos_urls);
    }
    
    // Combine media
    const mediaArray = [...images, ...videos];
    
    // Calculate discount (deterministic based on product ID)
    const discountPercent = (apiProduct.id % 5 === 0) 
        ? ((apiProduct.id % 30) + 5) 
        : 0;
    
    return {
        id: apiProduct.id,
        name: apiProduct.nom,
        price: apiProduct.prix,
        originalPrice: originalPrice,
        discountPercent: discountPercent,
        category: apiProduct.categorie,
        subcategory: apiProduct.subcategorie || '',
        images: mediaArray,
        videos: videos,
        description: apiProduct.description || '',
        sizes: apiProduct.taille_disponible || [],
        colors: apiProduct.couleur_disponible || [],
        stock: apiProduct.stock || 0,
        ordre: apiProduct.ordre || 9999
    };
}
```

---

## 3. **DOMContentLoaded Event & Initialization**

**File:** `index.html` - **Lines 5372-5428**

```javascript
document.addEventListener('DOMContentLoaded', function() {
    // Disable scroll during splash screen
    document.body.style.overflow = 'hidden';
    
    // Load products with intelligent caching system
    loadProductsFromApi();
    updateCartUI();
    checkAuth();
});
```

### Initialization Flow:
1. Show splash screen
2. Check if cache exists in localStorage
3. Load cached products first (if available)
4. Fetch fresh data from API simultaneously
5. Update UI with fresh data
6. Hide splash screen
7. Cache new data for next session

---

## 4. **Product Display Function**

**File:** `index.html` - **Lines 5461-5540+**

```javascript
function displayProducts(filter = 'all', reset = true) {
    if (reset) {
        currentPage = 1;
        currentFilter = filter;
    }
    
    const grid = document.getElementById('products-grid');
    
    let filteredProducts;
    
    // Filter by category
    if (filter !== 'all') {
        filteredProducts = allProducts.filter(p => {
            if (p.subcategory) {
                return p.category === filter || p.subcategory === filter;
            }
            return p.category === filter;
        });
    } else {
        filteredProducts = [...allProducts];
    }
    
    // Get products for current page
    const startIdx = (currentPage - 1) * productsPerPage;
    const endIdx = startIdx + productsPerPage;
    const productsToDisplay = filteredProducts.slice(startIdx, endIdx);
    
    // Create HTML for each product
    const html = productsToDisplay.map(product => createProductCard(product)).join('');
    grid.innerHTML = html;
    
    // Attach event listeners
    loadProductCardListeners();
}
```

---

## 5. **Current State: NO URL Parameter Handling**

### What's Missing:
- ❌ No `URLSearchParams` usage
- ❌ No URL query parameters like `?productId=36` or `?id=36`
- ❌ No deep linking capability
- ❌ No product detail pages
- ❌ No sharing links support
- ❌ No `location.search` or `window.location.hash` parsing

### Existing window.location Usage (for redirects only):
```javascript
window.location.href = 'login.html?autoGoogleLogin=true';  // For auth
window.location.href = 'welcome.html';                     // For redirects
```

---

## 6. **To Add Deep Linking, You'll Need:**

### Implementation Points:
1. **Parse URL parameters on page load** (before/after DOMContentLoaded)
2. **Create product detail modal/page** (currently products just appear in grid)
3. **Generate shareable links** with product IDs
4. **Scroll to/open product** when accessed via deep link

### Recommended Structure:
```javascript
// Check for product ID in URL
const urlParams = new URLSearchParams(window.location.search);
const productId = urlParams.get('productId') || urlParams.get('id');

document.addEventListener('DOMContentLoaded', function() {
    loadProductsFromApi().then(() => {
        if (productId) {
            const product = allProducts.find(p => p.id === parseInt(productId));
            if (product) {
                // Highlight/scroll to product or open modal
            }
        }
    });
});
```

---

## 7. **Key Variables & Functions Summary**

| Variable/Function | Type | Purpose |
|---|---|---|
| `allProducts` | Array | Main products data store from API |
| `currentFilter` | String | Current category filter ('all', 'mode', 'electronique', etc.) |
| `loadProductsFromApi()` | Function | Fetch products from API with caching |
| `mapApiProductToFrontend()` | Function | Transform API data to frontend format |
| `displayProducts()` | Function | Render products in grid |
| `createProductCard()` | Function | Generate HTML for single product |
| `loadProductCardListeners()` | Function | Attach click handlers to products |
| `cachedProducts` | localStorage | Stores products for offline access |

---

## 8. **API Endpoint Structure**

**Fetch URL:**
```
${window.API_BASE_URL}/produits?limit=500&offset=0
```

**Expected Response:**
```json
{
    "success": true,
    "produits": [
        {
            "id": 36,
            "nom": "Jean Carpenter",
            "prix": 10000,
            "categorie": "mode",
            "subcategorie": "homme",
            "images_urls": ["url1", "url2"],
            "videos_urls": [],
            "description": "...",
            "taille_disponible": [],
            "couleur_disponible": [],
            "stock": 10,
            "ordre": 1
        },
        ...
    ]
}
```

---

## 9. **Caching System**

**localStorage Keys:**
- `cachedProducts` - All products JSON
- `productsCacheTime` - Timestamp of cache
- `productsCacheInvalidated` - Flag to force refresh

---

## Ready for Deep Linking Implementation?

With this structure, you can:
1. ✅ Generate share links: `https://prestige-shop-express.onrender.com/?productId=36`
2. ✅ Create product detail pages/modals
3. ✅ Implement scroll-to-product functionality
4. ✅ Add product-specific analytics
5. ✅ Enable social media product cards (OG tags)
