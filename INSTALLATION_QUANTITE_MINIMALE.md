# 🚀 Installation Rapide - Quantité Minimale Prestige Business

## ⏱️ Temps estimé : 5 minutes

---

## 📋 Prérequis

- ✅ Accès à la base de données MySQL
- ✅ Fichiers du projet mis à jour
- ✅ Serveur Flask en cours d'exécution

---

## 🔧 Étapes d'installation

### 1️⃣ **Base de données** (2 minutes)

#### Option A : Via phpMyAdmin / Adminer

1. Ouvrez phpMyAdmin ou votre outil de gestion MySQL
2. Sélectionnez votre base de données
3. Cliquez sur l'onglet "SQL"
4. Copiez-collez le contenu de `add_quantite_minimale.sql`
5. Cliquez sur "Exécuter"

#### Option B : Via ligne de commande

```bash
# Se connecter à MySQL
mysql -u votre_utilisateur -p

# Sélectionner la base
USE nom_de_votre_base;

# Exécuter le script
source /chemin/vers/add_quantite_minimale.sql;
```

#### Option C : Via terminal (commande directe)

```bash
mysql -u votre_utilisateur -p nom_de_votre_base < add_quantite_minimale.sql
```

---

### 2️⃣ **Vérification** (1 minute)

Exécutez cette requête SQL :

```sql
SELECT 
    id, 
    nom, 
    categorie, 
    quantite_minimale 
FROM produits 
WHERE categorie = 'business'
LIMIT 5;
```

**Résultat attendu :**

| id | nom | categorie | quantite_minimale |
|----|-----|-----------|-------------------|
| 1  | Produit X | business | 5 |
| 2  | Produit Y | business | 10 |

✅ Si vous voyez des valeurs, c'est bon !  
❌ Si erreur, vérifiez que le script SQL a été exécuté.

---

### 3️⃣ **Déploiement Backend** (1 minute)

Le fichier `backend_render/server_fixed.py` est déjà mis à jour.

Si vous êtes en local :

```bash
# Redémarrer le serveur Flask
python backend_render/server_fixed.py
```

Si vous êtes sur Render ou autre hébergeur :

```bash
# Push vers Git
git add .
git commit -m "feat: Ajout quantité minimale Prestige Business"
git push origin main
```

---

### 4️⃣ **Déploiement Frontend** (1 minute)

Les fichiers suivants sont déjà mis à jour :

- ✅ `index.html`
- ✅ `admin/admin_produits.html`

Copiez-les simplement sur votre serveur :

```bash
# Exemple pour un déploiement FTP
scp index.html admin/admin_produits.html user@votre-serveur:/var/www/html/
```

Ou via Git :

```bash
git add .
git commit -m "feat: UI quantité minimale"
git push origin main
```

---

### 5️⃣ **Test final** (1 minute)

#### Test 1 : Dans l'admin

1. Allez sur `http://localhost:5000/admin/admin_produits.html`
2. Cliquez sur "Ajouter un produit"
3. Sélectionnez "💼 Prestige Business"
4. ✅ L'alerte orange doit apparaître
5. Remplissez "Quantité minimale" avec `10`
6. Sauvegardez

#### Test 2 : Sur le site client

1. Allez sur `http://localhost:5000/index.html`
2. Filtrez par catégorie "Prestige Business"
3. Trouvez un produit avec quantité minimale
4. ✅ Le badge orange doit apparaître sous le prix
5. Cliquez sur "Ajouter" avec quantité = 1
6. ❌ Une erreur doit s'afficher
7. Changez la quantité à 10 (ou plus)
8. ✅ Ça fonctionne !

#### Test 3 : Dans le panier

1. Ajoutez un produit business avec quantité = 10
2. Ouvrez le panier
3. Essayez de réduire à 9
4. ❌ Erreur "Quantité insuffisante"
5. ✅ Le minimum est bien bloqué

---

## 🎉 C'est terminé !

Votre fonctionnalité de quantité minimale est installée et opérationnelle.

---

## 🆘 Dépannage rapide

### Problème : "Column 'quantite_minimale' doesn't exist"

**Solution :**

```sql
ALTER TABLE produits 
ADD COLUMN quantite_minimale INT DEFAULT 1 AFTER ordre;
```

---

### Problème : "L'alerte ne s'affiche pas dans l'admin"

**Vérifications :**

1. La catégorie est-elle bien `"business"` ? (et non `"Prestige Business"`)
2. Avez-vous vidé le cache du navigateur ? (`Ctrl + F5`)
3. Vérifiez la console JavaScript (`F12`) pour les erreurs

---

### Problème : "La validation ne fonctionne pas"

**Vérifications :**

1. Dans `index.html`, cherchez la fonction `addToCart()`
2. Vérifiez que `quantiteMinimale` est présent dans `mapApiProductToFrontend()`
3. Rechargez la page avec `Ctrl + F5`

---

### Problème : "Les produits existants n'ont pas de quantité minimale"

**Solution :**

```sql
-- Mettre à jour tous les produits business
UPDATE produits 
SET quantite_minimale = 5 
WHERE categorie = 'business' 
  AND (quantite_minimale IS NULL OR quantite_minimale = 0);

-- Mettre à 1 pour les autres
UPDATE produits 
SET quantite_minimale = 1 
WHERE categorie != 'business' 
  AND (quantite_minimale IS NULL OR quantite_minimale = 0);
```

---

## 📊 Statut de l'installation

Cochez les cases au fur et à mesure :

- [ ] ✅ Script SQL exécuté
- [ ] ✅ Colonne `quantite_minimale` présente dans MySQL
- [ ] ✅ Backend déployé
- [ ] ✅ Frontend déployé
- [ ] ✅ Test admin réussi
- [ ] ✅ Test site client réussi
- [ ] ✅ Test panier réussi

---

## 📞 Besoin d'aide ?

Consultez le fichier `QUANTITE_MINIMALE_README.md` pour la documentation complète.

---

**Dernière mise à jour :** Mars 2026  
**Version :** 1.0
