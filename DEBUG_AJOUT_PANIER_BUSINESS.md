# 🔍 Débogage - Ajout au panier des produits Business

## 🎯 Objectif

Identifier pourquoi l'ajout au panier des produits "Prestige Business" ne fonctionne pas.

---

## 📋 Étapes de débogage

### Étape 1 : Ouvrir la console du navigateur

1. Allez sur `index.html`
2. Appuyez sur **F12** (ou clic droit → Inspecter)
3. Cliquez sur l'onglet **"Console"**

---

### Étape 2 : Tenter d'ajouter un produit business au panier

1. Trouvez un produit "Prestige Business"
2. Cliquez sur "Ajouter au panier"
3. **Observez la console**

---

### Étape 3 : Analyser les messages de debug

Vous devriez voir ce type de messages :

```javascript
🛒 Ajout au panier - Debug: {
    id: 123,
    name: "Montre de luxe",
    category: "business",        // ← Vérifiez cette valeur
    categorie: "💼 Prestige Business",  // ← Et celle-ci
    quantiteMinimale: 5,         // ← Quantité minimale
    quantite_minimale: undefined // ← Peut être undefined
}

📦 Est Business? true            // ← Doit être "true"
✅ Quantité minimale requise: 5  // ← La quantité minimale

📊 Quantité actuelle: 0 + 1 = 1 < minQty? true  // ← Si true, bloqué
```

---

## 🔎 Interprétation des résultats

### Cas 1 : Le message "🛒 Ajout au panier - Debug" n'apparaît PAS

**Problème :** La fonction `addToCart()` n'est pas appelée.

**Causes possibles :**
- ❌ Le bouton "Ajouter" n'a pas le bon `onclick`
- ❌ Une erreur JavaScript bloque avant l'appel
- ❌ Le produit n'a pas d'ID valide

**Solution :**
```javascript
// Dans la console, testez manuellement :
addToCart(ID_DU_PRODUIT);
```

---

### Cas 2 : `Est Business? false`

**Problème :** Le produit n'est pas reconnu comme "business".

**Valeurs dans la console :**
```javascript
category: "mode"           // ← Mauvaise catégorie
categorie: "💼 Prestige Business"  // ← Mais celle-ci est bonne
```

**Explication :** 
Le produit vient de la BDD avec `categorie: "💼 Prestige Business"` mais n'a pas été normalisé par `mapApiProductToFrontend()`.

**Solution :**
```sql
-- Vérifiez dans la BDD
SELECT id, nom, categorie FROM produits WHERE id = ID_DU_PRODUIT;
```

Si la catégorie est `"💼 Prestige Business"`, c'est que la normalisation ne se fait pas. Rechargez la page avec **Ctrl+Maj+R** (vidage cache).

---

### Cas 3 : `Quantité minimale requise: undefined` ou `0`

**Problème :** La quantité minimale n'est pas définie.

**Dans la console :**
```javascript
quantiteMinimale: undefined
quantite_minimale: undefined
```

**Cause :** 
Le champ `quantite_minimale` n'existe pas dans la base de données pour ce produit.

**Solution :**
```sql
-- Ajouter la colonne si elle n'existe pas
ALTER TABLE produits ADD COLUMN quantite_minimale INT DEFAULT 1;

-- Mettre à jour le produit
UPDATE produits SET quantite_minimale = 5 WHERE id = ID_DU_PRODUIT;
```

Puis rechargez la page.

---

### Cas 4 : `Quantité actuelle: 0 + 1 = 1 < minQty? true`

**Problème :** C'est le comportement NORMAL ! ✅

**Explication :**
- Quantité minimale requise : 5
- Vous essayez d'ajouter : 1
- Résultat : 1 < 5 → **BLOQUÉ** ✅

**Solution normale :**
L'utilisateur doit changer la quantité à 5 ou plus avant d'ajouter.

**Mais si vous voulez tester l'ajout :**
```javascript
// Dans la console, forcez l'ajout :
const product = allProducts.find(p => p.id === ID_DU_PRODUIT);
cart.push({...product, quantity: 5});
localStorage.setItem('cart', JSON.stringify(cart));
updateCartUI();
console.log('✅ Ajouté de force au panier');
```

---

### Cas 5 : Message d'erreur mais ajout quand même

**Problème :** La validation ne bloque pas vraiment.

**Dans la console :**
```javascript
⚠️ Vente en gros uniquement !
... puis ...
✅ Produit ajouté au panier !
```

**Cause :** Le code continue après le `return`.

**Vérification :**
Regardez s'il y a une autre fonction `addToCart()` qui serait appelée à la place.

**Solution :**
```javascript
// Cherchez toutes les occurrences de addToCart
grep -n "function addToCart" index.html
```

Devrait retourner **une seule ligne**.

---

## 🧪 Tests avancés

### Test A : Vérifier que la fonction est bien appelée

Dans la console :

```javascript
// Sauvegarder l'originale
const originalAddToCart = addToCart;

// Remplacer par une version tracée
addToCart = function(productId) {
    console.log('🔍 FONCTION APPELÉE AVEC ID:', productId);
    return originalAddToCart.call(this, productId);
};

// Maintenant essayez d'ajouter un produit
```

---

### Test B : Vérifier les données du produit

Dans la console :

```javascript
// Trouver TOUS les produits business
const businessProducts = allProducts.filter(p => 
    p.category === 'business' || 
    p.categorie === 'business' ||
    p.categorie === '💼 Prestige Business'
);

console.log('Produits business trouvés:', businessProducts.length);
console.table(businessProducts.map(p => ({
    id: p.id,
    name: p.name,
    category: p.category,
    categorie: p.categorie,
    quantiteMinimale: p.quantiteMinimale,
    quantite_minimale: p.quantite_minimale
})));
```

---

### Test C : Simuler un ajout manuel

Dans la console :

```javascript
// Choisir un produit business
const product = businessProducts[0];
console.log('Produit choisi:', product.name);

// Essayer de l'ajouter
console.log('Tentative d\'ajout...');
addToCart(product.id);

// Vérifier le panier
console.log('Panier actuel:', cart);
console.log('Nombre d\'articles:', cart.length);
```

---

## 🔧 Correctifs selon le diagnostic

### Problème : Produit non reconnu comme business

**Correctif :** Forcer la reconnaissance

```javascript
// Dans la console, après chargement de la page
allProducts.forEach(p => {
    if (p.categorie === '💼 Prestige Business' && p.category !== 'business') {
        console.log('Normalisation de:', p.name);
        p.category = 'business';
    }
});
```

---

### Problème : Quantité minimale manquante

**Correctif :** Définir une valeur par défaut

```javascript
// Dans la console
allProducts.forEach(p => {
    if (!p.quantiteMinimale && !p.quantite_minimale) {
        if (p.category === 'business' || p.categorie?.includes('Business')) {
            console.log('Définition quantité min par défaut pour:', p.name);
            p.quantiteMinimale = 5;
        }
    }
});
```

---

### Problème : Conflit de fonctions

**Correctif :** Trouver les doublons

```bash
# Dans un terminal Git Bash ou Linux
grep -n "function addToCart" "index.html"
```

Si plusieurs résultats, supprimez les doublons.

---

## 📊 Checklist de diagnostic

Cochez chaque élément vérifié :

- [ ] ✅ La console affiche "🛒 Ajout au panier - Debug"
- [ ] ✅ `Est Business?` affiche `true`
- [ ] ✅ `Quantité minimale requise:` affiche un nombre > 1
- [ ] ✅ Le message d'erreur s'affiche quand qty < minimum
- [ ] ✅ L'ajout fonctionne quand qty >= minimum
- [ ] ✅ Le panier se met à jour après ajout
- [ ] ✅ localStorage contient le panier

---

## 🆘 Commandes utiles

### Vider le cache et recharger

```javascript
// Dans la console
localStorage.clear();
sessionStorage.clear();
location.reload(true);
```

---

### Exporter les produits pour analyse

```javascript
// Sauvegarder tous les produits dans un fichier JSON
const dataStr = JSON.stringify(allProducts, null, 2);
const blob = new Blob([dataStr], {type: 'application/json'});
const url = URL.createObjectURL(blob);
const a = document.createElement('a');
a.href = url;
a.download = 'products_debug.json';
a.click();
console.log('✅ Fichier exporté');
```

---

### Importer des produits de test

```javascript
// Si vous avez un fichier JSON de test
fetch('products_test.json')
    .then(r => r.json())
    .then(products => {
        allProducts = products;
        console.log('✅ Produits importés:', products.length);
    });
```

---

## 📝 Exemple de rapport de bug

Quand vous signalez un problème, incluez :

```
=== DEBUG AJOUT PANIER ===

Produit : Montre Luxe
ID : 456
Category : "business"
Categorie : "💼 Prestige Business"
quantiteMinimale : 5
quantite_minimale : undefined

Console output :
🛒 Ajout au panier - Debug: {...}
📦 Est Business? true
✅ Quantité minimale requise: 5
📊 Quantité actuelle: 0 + 1 = 1 < minQty? true

Erreur affichée : "Vente en gros uniquement"

Comportement attendu : Changer quantité à 5
Comportement réel : Bloqué même à 5

Navigateur : Chrome 120
OS : Windows 11
```

---

## 🎯 Prochaines étapes

1. **Ouvrez la console (F12)**
2. **Essayez d'ajouter un produit business**
3. **Copiez-collez les messages de debug**
4. **Identifiez quel cas ci-dessus correspond à votre situation**
5. **Appliquez le correctif suggéré**

---

**Créé :** Mars 2026  
**Version :** 1.0  
**Objectif :** Déboguer l'ajout au panier des produits Business
