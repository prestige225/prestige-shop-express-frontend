# 📦 Fonctionnalité : Quantité Minimale - Prestige Business

## 🎯 Vue d'ensemble

Cette fonctionnalité permet de définir une **quantité minimale d'achat** pour les produits de la catégorie **"Prestige Business"** (vente en gros), similaire au fonctionnement d'Alibaba.

---

## 📋 Table des matières

1. [Base de données](#base-de-données)
2. [Backend (API)](#backend-api)
3. [Administration](#administration)
4. [Frontend (Site client)](#frontend-site-client)
5. [Validation et Sécurité](#validation-et-sécurité)
6. [Guide d'utilisation](#guide-dutilisation)

---

## 🗄️ Base de données

### Nouvelle colonne ajoutée

```sql
ALTER TABLE produits 
ADD COLUMN quantite_minimale INT DEFAULT 1 AFTER ordre;
```

### Script SQL d'installation

Exécutez le fichier `add_quantite_minimale.sql` :

```bash
mysql -u votre_utilisateur -p votre_base_de_donnees < add_quantite_minimale.sql
```

### Comportement

- **Valeur par défaut** : `1` (pas de minimum)
- **Pour "Prestige Business"** : Recommandé entre `5` et `100+`
- **Mise à jour automatique** : Les produits existants de catégorie "business" reçoivent automatiquement `quantite_minimale = 5`

---

## 🔌 Backend (API)

### Fichier modifié
`backend_render/server_fixed.py`

### Endpoints concernés

#### 1. **Création de produit** (`POST /api/produits`)

```python
quantite_minimale = int(data.get('quantite_minimale', 1))

INSERT INTO produits (..., quantite_minimale, ...)
VALUES (..., %s, ...)
```

#### 2. **Modification de produit** (`PUT /api/produits/<id>`)

```python
elif key in ('prix', 'stock', 'ordre', 'quantite_minimale'):
    champs.append(f"{key} = %s")
    valeurs.append(val)
```

#### 3. **Récupération de produits** (`GET /api/produits`)

Le champ `quantite_minimale` est automatiquement inclus dans la réponse JSON.

---

## 👨‍💼 Administration

### Fichier modifié
`admin/admin_produits.html`

### Nouvelles fonctionnalités

#### 1. **Champ de saisie "Quantité minimale"**

- Situé après "Ordre d'affichage"
- Type : `number`
- Minimum : `1`
- Défaut : `1`

#### 2. **Alerte contextuelle "Prestige Business"**

Lorsque la catégorie "💼 Prestige Business" est sélectionnée :

```html
<div class="bg-gradient-to-r from-orange-50 to-red-50 border-l-4 border-orange-500 p-4">
    <h4>📦 Produit Prestige Business</h4>
    <p>Ce produit est destiné à la vente en gros. La quantité minimale est <strong>obligatoire</strong>.</p>
</div>
```

#### 3. **Comportements intelligents**

- ✅ Affichage automatique de l'alerte orange quand catégorie = "business"
- ✅ Valeur par défaut forcée à `5` pour Prestige Business
- ✅ Message d'aide qui change selon la catégorie
- ✅ Rechargement correct lors de l'édition d'un produit

### Capture d'écran

```
┌─────────────────────────────────────────────┐
│ 💼 Prestige Business                        │
│ Ce produit est destiné à la vente en gros.  │
│ La quantité minimale est obligatoire.       │
└─────────────────────────────────────────────┘

Quantité minimale ⚠️
[5] ← Obligatoire pour "Prestige Business"
```

---

## 🌐 Frontend (Site client)

### Fichier modifié
`index.html`

### 1. **Affichage produit**

#### Badge "Vente en gros"

Pour les produits Prestige Business avec quantité minimale > 1 :

```html
<div class="bg-gradient-to-r from-orange-50 to-red-50 border-l-4 border-orange-500 p-2 rounded">
    <p><i class="fas fa-boxes"></i> Vente en gros uniquement</p>
    <p>Quantité minimale : <strong>5</strong> unités</p>
</div>
```

#### Emplacement
- Sous le prix
- Au-dessus du bouton "Ajouter au panier"

### 2. **Validation à l'ajout au panier**

#### Fonction `addToCart()`

```javascript
if (product.category === 'business' && product.quantiteMinimale > 1) {
    const currentQty = existingItem ? existingItem.quantity : 0;
    
    if (currentQty + 1 < product.quantiteMinimale) {
        showNotification(
            `⚠️ Vente en gros uniquement !
             Quantité minimale : ${product.quantiteMinimale} unités`,
            'error'
        );
        return; // Bloquer l'ajout
    }
}
```

### 3. **Validation dans le panier**

#### Fonction `updateQuantity()`

Empêche de réduire la quantité en dessous du minimum :

```javascript
if (item.category === 'business' && item.quantiteMinimale > 1) {
    const newQty = item.quantity + change;
    
    if (newQty < item.quantiteMinimale && newQty > 0) {
        showNotification(
            `⚠️ Quantité insuffisante !
             Minimum requis : ${item.quantiteMinimale} unités`,
            'error'
        );
        return; // Bloquer la réduction
    }
}
```

---

## 🔒 Validation et Sécurité

### Côté Client (Frontend)

✅ **Affichage clair** de la quantité minimale  
✅ **Blocage** de l'ajout si quantité < minimum  
✅ **Messages d'erreur** explicites  
✅ **Validation** dans le panier (boutons + / -)

### Côté Serveur (Backend)

⚠️ **Note importante** : Actuellement, la validation n'est faite que côté client.

Pour une sécurité maximale, vous pourriez ajouter :

```python
@app.route('/api/commandes', methods=['POST'])
def create_commande():
    data = request.get_json()
    
    for item in data.get('items', []):
        product = get_product_by_id(item['id'])
        
        if product.categorie == 'business' and product.quantite_minimale > 1:
            if item['quantity'] < product.quantite_minimale:
                return jsonify({
                    'success': False,
                    'error': f'Quantité minimale non respectée pour {product.nom}'
                }), 400
```

---

## 📖 Guide d'utilisation

### Pour l'administrateur

#### 1. **Ajouter un produit Prestige Business**

1. Allez sur `admin/admin_produits.html`
2. Sélectionnez la catégorie **"💼 Prestige Business"**
3. ⚠️ L'alerte orange apparaît automatiquement
4. Remplissez le champ **"Quantité minimale"** (ex: `10`)
5. Cliquez sur "Ajouter le produit"

#### 2. **Modifier un produit existant**

1. Cliquez sur "Modifier" sur un produit
2. Si c'est "Prestige Business", l'alerte s'affiche
3. Changez la quantité minimale si besoin
4. Sauvegardez

#### 3. **Recommandations**

| Type de produit | Quantité minimale conseillée |
|-----------------|------------------------------|
| Petit capital   | 5 - 10 unités                |
| Moyen capital   | 10 - 50 unités               |
| Gros capital    | 50 - 100+ unités             |

### Pour le client

#### 1. **Identification visuelle**

Les produits Prestige Business ont :
- 🟠 Un badge orange "Vente en gros uniquement"
- 📦 Mention "Quantité minimale : X unités"

#### 2. **Ajout au panier**

- Essayez d'ajouter 1 produit → ❌ Erreur
- Ajoutez la quantité minimale requise → ✅ Succès

#### 3. **Dans le panier**

- Bouton "-" bloqué si quantité = minimum
- Message d'erreur si tentative de réduction excessive

---

## 🎨 Personnalisation

### Changer les couleurs

Dans `index.html` et `admin/admin_produits.html` :

```css
/* Orange actuel */
bg-gradient-to-r from-orange-50 to-red-50
border-orange-500
text-orange-700

/* Bleu (exemple) */
bg-gradient-to-r from-blue-50 to-indigo-50
border-blue-500
text-blue-700
```

### Modifier le message d'erreur

Dans `index.html` :

```javascript
// Actuel
`⚠️ <strong>Vente en gros uniquement !</strong>
 Quantitée minimale : ${product.quantiteMinimale} unités`

// Personnalisé
`📦 <strong>Produit en gros uniquement !</strong>
 Minimum : ${product.quantiteMinimale} pièces requises`
```

---

## 🧪 Tests

### Scénarios à tester

1. ✅ Ajouter 1 unité d'un produit business (min 5) → ❌ Erreur
2. ✅ Ajouter 5 unités d'un produit business (min 5) → ✅ Succès
3. ✅ Réduire à 4 unités dans le panier → ❌ Erreur
4. ✅ Supprimer du panier → ✅ OK
5. ✅ Produit normal (non-business) → ✅ Pas de restriction

### Commandes MySQL de vérification

```sql
-- Voir tous les produits Prestige Business
SELECT id, nom, categorie, quantite_minimale 
FROM produits 
WHERE categorie = 'business'
ORDER BY quantite_minimale DESC;

-- Vérifier un produit spécifique
SELECT * FROM produits WHERE id = VOTRE_ID;
```

---

## 🚀 Déploiement

### 1. **Base de données**

```bash
mysql -u user -p database < add_quantite_minimale.sql
```

### 2. **Backend**

Déployez `backend_render/server_fixed.py` mis à jour

### 3. **Frontend**

Déployez `index.html` et `admin/admin_produits.html` mis à jour

### 4. **Vérification**

```bash
# Tester l'API
curl https://votre-api.com/api/produits | grep quantite_minimale

# Tester l'admin
https://votre-site.com/admin/admin_produits.html
```

---

## 📝 Notes techniques

### Compatibilité

- ✅ MySQL 5.7+
- ✅ Flask 2.0+
- ✅ JavaScript ES6+
- ✅ Tailwind CSS 3.0+

### Performances

- Impact frontend : **Négligeable** (quelques lignes JS)
- Impact backend : **Nul** (1 colonne INT en plus)
- Impact base de données : **Négligeable** (~4 bytes par produit)

### Évolutions futures possibles

- [ ] Validation backend renforcée
- [ ] Paliers de prix dégressifs selon quantité
- [ ] Export CSV des commandes avec validation quantité
- [ ] Alertes stock selon quantité minimale

---

## 🆘 Support

### Problèmes courants

#### "La colonne quantite_minimale n'existe pas"

→ Exécutez le script SQL `add_quantite_minimale.sql`

#### "L'alerte ne s'affiche pas dans l'admin"

→ Vérifiez que la catégorie est bien "business" (et non "Prestige Business")

#### "La validation ne fonctionne pas"

→ Vérifiez que `quantiteMinimale` est bien mappé dans `mapApiProductToFrontend()`

---

## ✅ Checklist d'installation

- [ ] Exécuter `add_quantite_minimale.sql`
- [ ] Vérifier que la colonne existe dans MySQL
- [ ] Déployer le backend mis à jour
- [ ] Déployer le frontend mis à jour
- [ ] Tester avec un produit Prestige Business
- [ ] Valider le blocage à l'ajout au panier
- [ ] Valider le blocage dans le panier
- [ ] Former l'équipe admin

---

**Développé pour Prestige Shop Express**  
*Version 1.0 - Mars 2026*
