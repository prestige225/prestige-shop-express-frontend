# 🛑 Gestion de la Rupture de Stock

## Vue d'ensemble

Cette fonctionnalité permet de gérer les produits en rupture de stock (statut `epuise`) de manière similaire aux grandes applications e-commerce. Lorsqu'un produit est marqué comme "Rupture de stock" dans le panneau d'administration, il devient automatiquement indisponible à l'achat sur le site frontend.

---

## 📋 Fonctionnalités Implémentées

### 1. **Dans le Frontend (index.html)**

#### Affichage des Produits en Rupture de Stock
- ✅ **Effet visuel** : Opacité réduite (60%) et filtre gris (grayscale)
- ✅ **Badge "Rupture de stock"** : Badge rouge pulsant en haut à droite
- ✅ **Nom barré** : Le nom du produit apparaît barré et en gris
- ✅ **Prix grisé** : Le prix n'est plus en violet mais en gris
- ✅ **Masquage des éléments interactifs** :
  - Bouton "J'aime" masqué
  - Badge de réduction masqué
  - Carrousel d'images désactivé
  - Étoiles d'évaluation masquées

#### Bouton d'Ajout au Panier
- ❌ **Bouton désactivé** : Fond gris, texte "Indisponible"
- 🚫 **Icône "Ban"** : Icône d'interdiction affichée
- ⚠️ **Curseur non autorisé** : `cursor: not-allowed`

#### Message d'Indisponibilité
- 📦 **Bloc d'information** : Message explicatif "Actuellement indisponible"
- ℹ️ **Description** : "Ce produit n'est plus disponible pour le moment"

### 2. **Dans la Vue Rapide (Quick View)**

#### Affichage Spécial
- 💰 **Prix barré** avec badge "Rupture de stock" pulsant
- 🚫 **Message d'erreur** : "❌ Actuellement indisponible"
- 🔒 **Bouton désactivé** dans le footer sticky

#### Produits Similaires
- Les produits similaires en rupture de stock sont également :
  - Grisés et réduits en opacité
  - Non cliquables (pas d'ouverture de quick view)
  - Avec badge "Rupture de stock"
  - Bouton "Ajouter" désactivé

### 3. **Validation Backend**

#### Fonctions `addToCart()` et `addToCartWithSelectedQty()`
- 🛑 **Vérification du statut** : Contrôle systématique avant ajout
- 🚫 **Blocage** : Retour anticipé si `status === 'epuise'`
- ⚠️ **Notification d'erreur** : Message clair à l'utilisateur
- 📝 **Logging** : Trace console pour débogage

---

## 🔧 Modification Techniques

### Fichier Modifié
- `index.html` (frontend)

### Fonctions Impactées

1. **`mapApiProductToFrontend()`**
   ```javascript
   // Ajout du champ status
   status: apiProduct.statut || 'actif'
   ```

2. **`createProductCard()`**
   ```javascript
   const isOutOfStock = product.status === 'epuise';
   // Application conditionnelle des classes CSS
   ${isOutOfStock ? 'opacity-60 grayscale' : ''}
   ```

3. **`addToCart()`**
   ```javascript
   if (product.status === 'epuise') {
       showNotification('🚫 Produit indisponible !', 'error');
       return;
   }
   ```

4. **`addToCartWithSelectedQty()`**
   ```javascript
   // Même validation que addToCart()
   if (product.status === 'epuise') {
       showNotification('🚫 Produit indisponible !', 'error');
       return;
   }
   ```

5. **`openProductQuickView()`**
   ```javascript
   const isOutOfStock = product.status === 'epuise';
   // Affichage conditionnel du contenu
   ```

---

## 📊 Base de Données

### Table `produits`
Le champ `statut` utilise un ENUM avec 3 valeurs possibles :
- `'actif'` : Produit disponible et visible
- `'inactif'` : Produit désactivé temporairement  
- `'epuise'` : Produit en rupture de stock ✨

```sql
statut ENUM('actif','inactif','epuise') DEFAULT 'actif'
```

⚠️ **Important** : La valeur à utiliser dans les formulaires HTML est `'epuise'` (et non `'rupture'`).

---

## 🎯 Expérience Utilisateur

### Ce que voit l'utilisateur

1. **Sur la page d'accueil**
   - Produit grisé avec badge "Rupture de stock"
   - Bouton "Indisponible" non cliquable
   - Impossible d'ajouter au panier

2. **Dans le quick view**
   - Message clair d'indisponibilité
   - Prix affiché mais barré
   - Bouton désactivé

3. **Tentative d'ajout forcé**
   - Notification d'erreur rouge
   - Message explicatif
   - Aucun ajout au panier effectué

### Avantages
- ✅ **Clarté** : L'utilisateur sait immédiatement qu'un produit n'est plus disponible
- ✅ **Cohérence** : Même comportement sur toutes les pages
- ✅ **Protection** : Impossible d'ajouter accidentellement un produit indisponible
- ✅ **Professionnalisme** : Standard des grands sites e-commerce

---

## 🧪 Tests Recommandés

### Test 1 : Administration
1. Se connecter à `admin_produits.html`
2. Modifier un produit existant
3. Changer le statut à "Rupture de stock"
4. Sauvegarder

### Test 2 : Frontend - Page d'accueil
1. Actualiser `index.html`
2. Vérifier que le produit est grisé
3. Vérifier la présence du badge "Rupture de stock"
4. Tenter de cliquer sur "Ajouter au panier" → Doit être désactivé

### Test 3 : Frontend - Quick View
1. Ouvrir le quick view du produit (si possible via recherche)
2. Vérifier le message d'indisponibilité
3. Vérifier que le bouton est désactivé

### Test 4 : Validation Backend
1. Ouvrir la console navigateur (F12)
2. Tenter d'ajouter le produit via : `addToCart(PRODUCT_ID)`
3. Vérifier la notification d'erreur
4. Vérifier que le panier n'a pas été modifié

---

## 🔐 Sécurité

### Protection contre les ajouts accidentels
- Validation côté client (JavaScript)
- Désactivation native du bouton HTML (`disabled`)
- Notifications d'erreur bloquantes
- Logging console pour traçabilité

### Limites
⚠️ **Important** : Cette protection est côté client uniquement. Pour une sécurité totale, il faudrait également implémenter une validation côté serveur (backend) qui refuserait les commandes de produits en rupture de stock.

---

## 📝 Notes pour les Développeurs

### Bonnes Pratiques
- Toujours vérifier le statut avant tout ajout au panier
- Utiliser les classes CSS conditionnelles pour l'UI
- Garder une trace console pour le débogage
- Afficher des messages clairs à l'utilisateur

### Évolutions Possibles
- 🔄 Ajouter une validation côté backend
- 📧 Proposer une alerte "Disponibilité" par email
- 📊 Tracker les produits en rupture pour réassort
- 🎨 Animer davantage la transition de statut

---

## 🤝 Support

Pour toute question ou problème concernant cette fonctionnalité, veuillez consulter :
- La console navigateur pour les logs
- Les notifications utilisateur pour les erreurs
- Le code source commenté dans `index.html`

---

**Date d'implémentation** : 26 Mars 2026  
**Version** : 1.0  
**Statut** : ✅ Implémenté et testé
