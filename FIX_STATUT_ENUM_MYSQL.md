# 🔧 Correction Erreur MySQL - Data Truncated for Column 'statut'

## ❌ Problème Rencontré

**Erreur MySQL :**
```
Error: 1265 (01000): Data truncated for column 'statut' at row 1
```

### Cause du Problème

Il y avait une **incohérence** entre :
- La valeur envoyée par le formulaire HTML : `"rupture"`
- La valeur attendue par l'ENUM MySQL : `"epuise"`

---

## 🔍 Analyse

### Structure de la Table `produits`

```sql
statut ENUM('actif','inactif','epuise') DEFAULT 'actif'
```

L'ENUM MySQL accepte uniquement 3 valeurs :
1. `'actif'`
2. `'inactif'`
3. `'epuise'`

### Formulaire dans `admin_produits.html` (AVANT)

```html
<select id="product-status">
    <option value="actif">Actif</option>
    <option value="inactif">Inactif</option>
    <option value="rupture">Rupture de stock</option>  <!-- ❌ VALEUR INCORRECTE -->
</select>
```

**Problème** : La valeur `"rupture"` n'existe pas dans l'ENUM MySQL, donc rejet de la requête.

---

## ✅ Solution Appliquée

### 1. Correction du Formulaire HTML

**Fichier** : `admin_produits.html`

**Avant** (ligne 153) :
```html
<option value="rupture">Rupture de stock</option>
```

**Après** :
```html
<option value="epuise">Rupture de stock</option>
```

### 2. Correction des Comparaisons JavaScript

**Fichier** : `admin_produits.html`

**Avant** (ligne 450) :
```javascript
product.statut === 'rupture' ? 'red' : 'yellow'
```

**Après** :
```javascript
product.statut === 'epuise' ? 'red' : 'yellow'
```

---

## 📝 Fichiers Modifiés

### `admin_produits.html`
- ✅ Ligne 153 : Changé `value="rupture"` → `value="epuise"`
- ✅ Ligne 450 : Changé comparaison `'rupture'` → `'epuise'`

### `FIX_RUPTURE_DE_STOCK.md`
- ✅ Ajout d'une note importante sur la valeur correcte à utiliser

---

## 🎯 Résultat

Maintenant, quand vous sélectionnez "Rupture de stock" dans l'admin :

1. **Formulaire** envoie la valeur `"epuise"` ✅
2. **MySQL** accepte la valeur dans l'ENUM ✅
3. **Backend** peut sauvegarder sans erreur ✅
4. **Frontend** affiche correctement le statut ✅

---

## 🧪 Comment Vérifier

### Test de Validation

1. **Ouvrir** `admin_produits.html`
2. **Modifier** un produit existant
3. **Sélectionner** "Rupture de stock" dans le dropdown
4. **Sauvegarder** le produit
5. **Vérifier** dans la base de données :

```sql
SELECT id, nom, statut FROM produits WHERE statut = 'epuise';
```

**Résultat attendu** : Le produit doit avoir `statut = 'epuise'` (et non `NULL` ou erreur)

---

## 💡 Bonne Pratique

**Toujours vérifier** que les valeurs des formulaires HTML correspondent exactement aux valeurs définies dans :
- Les ENUM MySQL
- Les validations backend
- Les constantes frontend

**Règle** : 
- HTML `value="xxx"` = MySQL `ENUM('xxx')`
- Utiliser la même chaîne exacte (sensible à la casse)

---

## 🔄 Migration des Données Existantes

Si vous aviez déjà des produits avec le statut `"rupture"` (avant correction), vous devrez peut-être les mettre à jour :

```sql
-- Vérifier s'il y a des produits avec un statut incorrect
SELECT * FROM produits WHERE statut NOT IN ('actif', 'inactif', 'epuise');

-- Si nécessaire, corriger les anciennes valeurs
UPDATE produits SET statut = 'epuise' WHERE statut = 'rupture';
```

⚠️ **Note** : MySQL devrait rejeter toute valeur hors de l'ENUM, donc cette situation ne devrait pas se produire sauf si l'ENUM a été modifié récemment.

---

## 📚 Leçons Apprises

1. **Valider les ENUMs** : Toujours vérifier les valeurs possibles dans la BDD
2. **Tests de validation** : Tester chaque valeur possible avant déploiement
3. **Documentation** : Noter les valeurs acceptées dans le code
4. **Cohérence** : Utiliser les mêmes chaînes partout (frontend, backend, BDD)

---

## ✅ Statut

**Problème** : ❌ Identifié  
**Correction** : ✅ Appliquée  
**Testé** : ⏳ En attente de validation  

---

**Date de correction** : 26 Mars 2026  
**Version** : 1.1  
**Impact** : Mineur (formulaire admin uniquement)
