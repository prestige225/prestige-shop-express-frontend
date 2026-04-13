# 🧪 GUIDE DE TEST - Badge Prestige Business

## 📋 Checklist Complète

### Phase 1️⃣: Préparation

- [ ] Ouvrir le fichier [index.html](index.html) dans l'éditeur
- [ ] Vérifier que les corrections sont présentes:
  - [ ] Fonction `isBusinessProduct()` au ligne ~5567
  - [ ] Console.logs ajoutés dans `normalizeProduct()` 
  - [ ] Console.logs dans `loadProducts()`
- [ ] Ouvrir le fichier [FIX_QUANTITE_MINIMALE_PRESTIGE.sql](FIX_QUANTITE_MINIMALE_PRESTIGE.sql)

---

### Phase 2️⃣: Exécution du Fix SQL (CRUCIAL)

**⚠️ OBLIGATOIRE si les nouveaux produits n'affichent pas le badge**

#### Option A: Via PhpMyAdmin (meilleur)
1. Accédez à votre PhpMyAdmin (Render)
2. Sélectionnez votre base de données `prestige_shop`
3. Allez à l'onglet **SQL**
4. Copiez le contenu de `FIX_QUANTITE_MINIMALE_PRESTIGE.sql`
5. Exécutez la requête
6. Vérifiez le message: "✅ Colonne quantite_minimale mise à jour"

#### Option B: Via línea de commande MySQL
```bash
mysql -u [root] -p [database_name] < FIX_QUANTITE_MINIMALE_PRESTIGE.sql
```

#### Vérifier le succès
Exécutez cette requête pour confirmer:
```sql
SELECT 
    COUNT(*) as total_business,
    COUNT(CASE WHEN quantite_minimale >= 3 THEN 1 END) as with_qty3
FROM produits 
WHERE categorie LIKE '%Prestige Business%'
   OR categorie = 'business';
```

**Résultat attendu:** `with_qty3` = `total_business` (tous les Business ont min qty >= 3)

---

### Phase 3️⃣: Test en Local/Développement

#### 1. Démarrer votre serveur local
```bash
# Terminal
python app.py
# OU si vous utilisez gunicorn
gunicorn app:app
```

#### 2. Ouvrir votre navigateur
```
URL: http://localhost:5000 (ou votre port)
```

#### 3. Ouvrir la Console (F12)
- Appuyez sur `F12`
- Allez à l'onglet **Console**
- Rechargez la page: `Ctrl + R` ou `Cmd + R`

#### 4. Vérifier les logs Business

**À voir dans la console:**
```
🏢 PRODUITS BUSINESS DEPUIS L'API: Array(3)
  0: {id: 25, nom: "Chemisier Business Premium", categorie_api: "💼 Prestige Business", quantite_minimale_api: 3}
  1: {id: 42, nom: "Suite de Bureau", categorie_api: "💼 Prestige Business", quantite_minimale_api: 3}
  2: {id: 58, nom: "Accessoire Gros", categorie_api: "💼 Prestige Business", quantite_minimale_api: 3}

✅ PRODUITS BUSINESS NORMALISÉS: Array(3)
  0: {id: 25, nom: "Chemisier Business Premium", category_normalisee: "business", quantiteMinimale: 3, badge_display: "✓ Badge affichable"}
  1: {id: 42, nom: "Suite de Bureau", category_normalisee: "business", quantiteMinimale: 3, badge_display: "✓ Badge affichable"}
  2: {id: 58, nom: "Accessoire Gros", category_normalisee: "business", quantiteMinimale: 3, badge_display: "✓ Badge affichable"}

🏢 PRODUIT BUSINESS DÉTECTÉ: 
  id: 25
  nom: "Chemisier Business Premium"
  categorie_brute: "💼 Prestige Business"
  categorie_normalisee: "business"
  quantite_minimale_brute: 3
  quantite_minimale_normalisee: 3
  affichage_badge: true ✓
```

**Si vous voyez ces logs:** ✅ **Étape réussie!**

---

### Phase 4️⃣: Test Affichage du Badge

#### 4.1 Vérifier sur la liste des produits

1. Accédez à la **page d'accueil**
2. Cherchez un produit avec la catégorie **"💼 Prestige Business"**
3. **Vous devriez voir:**
   - ✅ Un badge orange en bas de la carte produit
   - ✅ Texte: `Vente en gros uniquement`
   - ✅ Ligne 2: `Quantité minimale : 3 unités`

**Exemple d'apparence:**
```
┌─────────────────────────┐
│     [Image de laProduit] │
│                         │
│ Categorie: Prestige Business
│ ⭐⭐⭐⭐⭐              │
│ 15,000 FCFA             │
│ ┏━━━━━━━━━━━━━━━━━━━┓ │
│ ┃📦 Vente en gros   ┃ │
│ ┃Quantité min: 3    ┃ │
│ ┗━━━━━━━━━━━━━━━━━━━┛ │
│ [Ajouter au panier]     │
└─────────────────────────┘
```

#### 4.2 Vérifier sur la page détail du produit

1. Cliquez sur un produit Business
2. Allez a la section **"Détails du produit"**
3. **Vous devriez voir:**
   - ✅ Un grand encadré orange avec les détails Business
   - ✅ Titre: `Vente en gros uniquement`
   - ✅ Icône 📦 et 🚚
   - ✅ Texte explicatif complet

---

### Phase 5️⃣: Test Interaction Panier

#### Test 1: Sélectionner une quantité insuffisante

1. Sur la page détail d'un produit Business
2. **Sélectionnez: 2 unités** (min = 3)
3. Cliquez sur **"Ajouter au panier"**
4. **Vous devriez voir:**
   - ⚠️ Alerte rouge: "Vente en gros uniquement !"
   - ⚠️ Message: "Quantité minimale requise : 3 unités"
   - ⚠️ Bouton est BLOQUÉ (pas d'ajout)

**Console montre:** `📦 Est Business? true | quantityToAdd: 2 < minQty: 3 ✓ BLOQUÉ`

#### Test 2: Sélectionner une quantité suffisante

1. **Sélectionnez: 5 unités** (✓ >= 3)
2. Cliquez sur **"Ajouter au panier"**
3. **Vous devriez voir:**
   - ✅ Produit ajouté au panier
   - ✅ Message de succès (vert)
   - ✅ Panier met à jour le nombre d'articles

**Console montre:** `✅ Quantité minimale requise: 3 | AJOUT OK`

#### Test 3: Modifier la quantité dans le panier

1. Allez au **panier** (icône 🛒)
2. Trouvez un produit Business
3. Essayez de **réduire** sa quantité en-dessous du minimum
4. **Vous devriez voir:**
   - ⚠️ Alerte: "Quantité insuffisante !"
   - ⚠️ Le bouton `-` est bloqué
   - ✅ Vous pouvez toujours augmenter avec `+`

**Console montre:** `⚠️ Quantité insuffisante ! Minimum requis : 3 unités`

---

### Phase 6️⃣: Test Visuel Complet

#### Checklist visuelle

- [ ] Badge orange visible sur la liste des produits
- [ ] Badge affiche correctement "Vente en gros uniquement"
- [ ] Quantité minimale affichée (3, 5, etc.)
- [ ] Icônes (📦, 🚚) présentes et lisibles
- [ ] Sélecteur de quantité limité au minimum requis
- [ ] Texte en français correct, sans encodage
- [ ] Badge disparaît pour les produits non-Business
- [ ] Badge disparaît si quantite_minimale = 1

---

## 🔴 Dépannage - Si le badge n'affiche pas

### Étape 1: Vérifier les logs

```javascript
// Dans la console (F12), cherchez:
// ✅ Les 3 logs de debug apparaissent?
// - 🏢 PRODUITS BUSINESS DEPUIS L'API
// - ✅ PRODUITS BUSINESS NORMALISÉS  
// - 🏢 PRODUIT BUSINESS DÉTECTÉ
```

**Si les logs n'apparaissent PAS:**
- Problème: Pas de produits Business en BDD avec la catégorie correcte
- Solution: Vérifiez que vos produits ont `categorie = '💼 Prestige Business'` (exact)
- SQL à exécuter pour vérifier:
```sql
SELECT id, nom, categorie, quantite_minimale FROM produits WHERE categorie LIKE '%Business%';
```

---

### Étape 2: Vérifier la base de données

**Si les logs MONTRENT les produits Business, mais le badge ne s'affiche pas:**

1. Ouvrez la console et copiez une ligne du log:
```javascript
// Exemple:
{id: 25, nom: "...", quantite_minimale_api: 3}
```

2. Exécutez en console:
```javascript
// Cherchez manuellement le produit
const prod = allProducts.find(p => p.id === 25);
console.log('Détails complets:', prod);
console.log('isBusinessProduct?', isBusinessProduct(prod));
console.log('quantiteMinimale > 1?', prod.quantiteMinimale > 1);
console.log('Badge doit s\'afficher?', isBusinessProduct(prod) && prod.quantiteMinimale > 1);
```

3. Vérifiez les résultats - au moins 2 doivent être `true`:
   - `isBusinessProduct? true`
   - `quantiteMinimale > 1? true`
   - `Badge doit s'afficher? true`

**Si l'un est false:**
- `isBusinessProduct = false` → Catégorie mal nommée en BDD
- `quantiteMinimale > 1 = false` → quantité_minimale n'a pas été mise à jour (exécutez le SQL fix)

---

### Étape 3: Vérifier le cache navigateur

```javascript
// Dans la console:
// 1. Vider le cache:
localStorage.clear();
sessionStorage.clear();

// 2. Recharger:
location.reload();

// 3. Vérifiez les logs à nouveau
```

---

## ✅ Signes que tout fonctionne

| Signe | ✅ OK | ❌ Problème |
|-------|--------|-----------|
| Logs de debug affichés | Oui | Pas de logs = pas de Business en BDD |
| Badge visible | Oui | Invisible = quantité_minimale = 1 |
| Ajout au panier bloqué (qty < min) | Bloqué | Pas bloqué = fonction helper non utilisée |
| Message d'alerte | Oui | Non = message d'alerte não affiché |
| Panier met à jour | Oui | Non = ajout non enregistré |

---

## 📊 Résumé des Tests Effectués

Remplissez ce tableau après vos tests:

```
| Test | Statut | Détails |
|------|--------|---------|
| Logs debug affiché | ☐ OK ☐ NOK | |
| Badge sur liste produits | ☐ OK ☐ NOK | |
| Badge sur page détail | ☐ OK ☐ NOK | |
| Ajout au panier (qty < min) | ☐ BLOQUÉ OK | |
| Ajout au panier (qty >= min) | ☐ OK ☐ NOK | |
| Modification panier | ☐ VALIDATION OK | |
| Message alerte français | ☐ OK ☐ NOK | |
| Pas de badge pour non-Business | ☐ OK ☐ NOK | |
```

---

## 🚀 Déploiement vers Render

Une fois les tests locaux passés:

1. **Commit vos changements:**
   ```bash
   git add index.html FIX_QUANTITE_MINIMALE_PRESTIGE.sql
   git commit -m "fix: Amélioration détection Prestige Business avec fonction helper robuste"
   git push origin main
   ```

2. **Render redéploie automatiquement**
   - Vérifiez le statut dans le dashboard Render
   - Attendez ~5 min que le déploiement se termine

3. **Vérifiez en production:**
   - Ouvrez `https://prestige-shop-express.onrender.com`
   - Ouvrez la Console (F12)
   - Vérifiez les logs de debug

4. **Exécutez le SQL de correction:**
   - Si ce n'est pas fait localement, exécutez `FIX_QUANTITE_MINIMALE_PRESTIGE.sql` sur votre BDD Render

---

## 📝 Notes

- Les corrections de code JavaScript sont IMMÉDIATEMENT en vigueur après déploiement
- La correction SQL de la BDD ne prend effet que sur les NOUVEAUX produits ou ceux modifiés
- Les produits existants gardent leur `quantite_minimale` existante

---

**Besoin d'aide?** 
- Vérifiez les logs de la console (F12)
- Consultez le fichier [FIX_BADGE_PRESTIGE_BUSINESS_COMPLET.md](FIX_BADGE_PRESTIGE_BUSINESS_COMPLET.md)
- Exécutez les requêtes SQL de démonstration dans votre PhpMyAdmin

Version: 2026-04-05
