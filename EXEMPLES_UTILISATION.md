# 💡 Exemples d'utilisation - Quantité Minimale

## 📋 Table des matières

1. [Exemples pour l'admin](#exemples-pour-ladmin)
2. [Exemples pour le client](#exemples-pour-le-client)
3. [Cas pratiques](#cas-pratiques)
4. [Bonnes pratiques](#bonnes-pratiques)

---

## 👨‍💼 Exemples pour l'admin

### Exemple 1 : Produit "Lot de 10 montres de luxe"

**Configuration :**

```
Catégorie : 💼 Prestige Business
Sous-catégorie : Accessoires de luxe
Nom : Lot de 10 montres automatiques
Prix unitaire : 15 000 FCFA
Quantité minimale : 10
Stock : 100
```

**Résultat :**
- Le client doit acheter **au minimum 10 unités**
- Commande minimum : 15 000 × 10 = **150 000 FCFA**
- Badge affiché : "Quantité minimale : 10 unités"

---

### Exemple 2 : "Sac à main en cuir - Vente en gros"

**Configuration :**

```
Catégorie : 💼 Prestige Business
Sous-catégorie : Maroquinerie
Nom : Sac à main cuir véritable (lot de 5)
Prix unitaire : 8 000 FCFA
Quantité minimale : 5
Stock : 50
```

**Résultat :**
- Achat minimum : 5 sacs
- Commande minimum : 8 000 × 5 = **40 000 FCFA**

---

### Exemple 3 : "Écouteurs Bluetooth - Grossiste"

**Configuration :**

```
Catégorie : 💼 Prestige Business
Sous-catégorie : Électronique
Nom : Écouteurs sans fil TWS (carton de 20)
Prix unitaire : 3 000 FCFA
Quantité minimale : 20
Stock : 200
```

**Résultat :**
- Achat minimum : 20 écouteurs
- Commande minimum : 3 000 × 20 = **60 000 FCFA**

---

### Exemple 4 : "Vêtements en gros"

**Configuration :**

```
Catégorie : 💼 Prestige Business
Sous-catégorie : Mode femme
Nom : Robe d'été fluide (par 6 pièces)
Prix unitaire : 5 000 FCFA
Quantité minimale : 6
Tailles disponibles : S, M, L, XL
Couleurs : Bleu, Rouge, Vert
Stock : 60
```

**Résultat :**
- Achat minimum : 6 robes
- Commande minimum : 5 000 × 6 = **30 000 FCFA**
- Le client peut mixer tailles et couleurs

---

## 🛒 Exemples pour le client

### Scénario 1 : Client veut tester avec 1 unité

**Action :**
1. Client voit : "Quantité minimale : 10 unités"
2. Clique sur "Ajouter" (quantité par défaut = 1)
3. ❌ **Erreur affichée :**
   ```
   ⚠️ Vente en gros uniquement !
   Quantité minimale : 10 unités
   Pour ce produit Prestige Business.
   ```

**Résultat :** Le client comprend qu'il doit commander 10 unités minimum.

---

### Scénario 2 : Client respecte la quantité minimale

**Action :**
1. Client change la quantité à **10**
2. Clique sur "Ajouter"
3. ✅ **Succès :**
   ```
   Produit ajouté au panier ! 🎉
   ```
4. Confettis animés

**Résultat :** Produit ajouté avec 10 unités.

---

### Scénario 3 : Client dans le panier

**Situation :**
- Panier contient : 10 unités du produit business
- Client essaie de réduire à 9

**Action :**
1. Clique sur bouton "-"
2. ❌ **Erreur :**
   ```
   ⚠️ Quantité insuffisante !
   Minimum requis : 10 unités
   Pour ce produit Prestige Business.
   ```

**Résultat :** La quantité reste bloquée à 10 minimum.

---

### Scénario 4 : Produit normal vs Business

**Comparaison :**

| Produit | Catégorie | Quantité min | Résultat |
|---------|-----------|--------------|----------|
| T-shirt | Mode | 1 (défaut) | ✅ Achat libre |
| Lot T-shirts (grossiste) | Business | 20 | ❌ Bloqué à 20 |

---

## 🎯 Cas pratiques

### Cas 1 : Revendeur veut compléter son stock

**Profil :** Commerçant à Abidjan  
**Besoin :** Recompléter son rayon accessoires  
**Budget :** 200 000 FCFA

**Commande type :**

```
Produit 1 : Lot de 10 montres × 15 000 = 150 000 FCFA
Produit 2 : Sac à main cuir × 5 = 40 000 FCFA
Total : 190 000 FCFA ✅
```

**Avantage :** Grâce aux quantités minimales, le revendeur sait qu'il aura assez de stock.

---

### Cas 2 : Particulier veut un seul produit

**Profil :** Étudiant  
**Besoin :** Acheter 1 écouteur pour lui  
**Budget :** 5 000 FCFA

**Découverte :**
- Voit : "Écouteurs TWS - 3 000 FCFA"
- Mais : "Quantité minimale : 20 unités"
- Calcul : 3 000 × 20 = 60 000 FCFA ❌

**Alternatives :**
1. Se rabat sur un produit non-business
2. Se groupe avec des amis pour acheter 20 unités
3. Contacte le vendeur pour un arrangement

---

### Cas 3 : Association fait un achat groupé

**Profil :** Association de femmes entrepreneures  
**Besoin :** Sacs à main pour revente  
**Budget : 500 000 FCFA

**Commande :**

```
Sac à main cuir × 50 unités
(Paquet de 5 × 10 fois)
Prix : 8 000 × 50 = 400 000 FCFA ✅

Reste : 100 000 FCFA pour autres produits
```

**Avantage :** Les quantités minimales garantissent des prix de gros.

---

## 📊 Bonnes pratiques

### Pour les administrateurs

#### ✅ À FAIRE

1. **Définir des minimums réalistes**
   ```
   Petit capital : 5 - 10 unités
   Moyen capital : 10 - 50 unités
   Gros capital : 50 - 100+ unités
   ```

2. **Indiquer clairement dans le nom**
   ```
   ✅ "Lot de 10 montres"
   ✅ "Carton de 20 écouteurs"
   ❌ "Montre" (trop vague)
   ```

3. **Adapter le stock**
   ```
   Si qty_min = 20
   Alors stock >= 100 (pour avoir de la marge)
   ```

4. **Prix attractifs**
   ```
   Prix unitaire business < Prix unitaire détail
   Exemple : 
   - Détail : 5 000 FCFA
   - Business (min 10) : 3 500 FCFA
   ```

#### ❌ À ÉVITER

1. **Minimums trop élevés**
   ```
   ❌ Quantité minimale : 1000 (décourageant)
   ✅ Quantité minimale : 50 (raisonnable)
   ```

2. **Oublier de mettre à jour le stock**
   ```
   ❌ qty_min = 20 mais stock = 15
   ✅ Toujours stock >= qty_min
   ```

3. **Mettre tous les produits en "business"**
   ```
   ❌ Tout le catalogue en vente en gros
   ✅ Seulement les produits éligibles
   ```

---

### Pour les clients

#### ✅ Conseils d'achat

1. **Vérifier la quantité minimale avant d'ajouter**
   ```
   Cherchez le badge orange :
   "Quantité minimale : X unités"
   ```

2. **Calculer le total minimum**
   ```
   Prix × Quantité minimale = Total minimum
   ```

3. **Se grouper si nécessaire**
   ```
   Trop cher tout seul ?
   → Proposez à des amis de se cotiser
   ```

4. **Contacter le vendeur pour gros volumes**
   ```
   Besoin de 500 unités ?
   → Message pour négociation possible
   ```

---

## 🎨 Templates de configuration

### Template 1 : Petit revendeur

```
Nom : [Produit] - Lot de 10
Catégorie : 💼 Prestige Business
Prix : [Votre prix] / 1.3 (pour laisser une marge)
Quantité minimale : 10
Description : "Idéal pour démarrer votre activité. Lot économique de 10 pièces."
```

---

### Template 2 : Grossiste

```
Nom : [Produit] - Carton de 50
Catégorie : 💼 Prestige Business
Prix : [Prix très compétitif]
Quantité minimale : 50
Description : "Prix grossiste. Carton scellé de 50 unités. Parfait pour revendeurs."
```

---

### Template 3 : Demi-gros

```
Nom : [Produit] - Pack de 20
Catégorie : 💼 Prestige Business
Prix : [Prix intermédiaire]
Quantité minimale : 20
Description : "Pack découverte pour petits commerçants. 20 pièces assorties."
```

---

## 📈 Stratégies commerciales

### Stratégie 1 : Escalade de prix

```
Quantité 1-9 : 5 000 FCFA (détail - non disponible)
Quantité 10-49 : 4 000 FCFA (petit grossiste)
Quantité 50+ : 3 500 FCFA (gros grossiste)
```

**Implémentation future possible :**
- Créer plusieurs produits avec quantités différentes
- Ou ajouter un système de paliers

---

### Stratégie 2 : Mix & Match

```
Produit : Assortiment chaussures
Quantité minimale : 10 paires
Règle : Peut mixer tailles et modèles
```

**Avantage :** Le client peut varier sans être bloqué.

---

### Stratégie 3 : Saisonnière

```
Haute saison : qty_min = 20
Basse saison : qty_min = 10
Promotion : qty_min = 5
```

**Gestion :** L'admin modifie selon la période.

---

## 🔧 Astuces techniques

### Pour l'admin

**Astuce 1 : Mise à jour en masse**

```sql
-- Augmenter tous les minimums de 10%
UPDATE produits 
SET quantite_minimale = ROUND(quantite_minimale * 1.1)
WHERE categorie = 'business';
```

**Astuce 2 : Voir les performances**

```sql
-- Produits business les plus vendus
SELECT 
    p.nom,
    p.quantite_minimale,
    COUNT(c.id) as nombre_commandes
FROM produits p
JOIN commandes c ON p.id = c.produit_id
WHERE p.categorie = 'business'
GROUP BY p.id
ORDER BY nombre_commandes DESC;
```

---

## 💬 FAQ

### Q: Puis-je changer la quantité minimale après coup ?

**R:** Oui ! Modifiez simplement le champ dans l'admin. Les nouvelles commandes prendront en compte la nouvelle valeur.

---

### Q: Que se passe-t-il si un client a déjà le produit dans son panier et je change le minimum ?

**R:** Le client pourra toujours modifier son panier, mais sera bloqué s'il essaie de passer en dessous du nouveau minimum.

---

### Q: Puis-je désactiver temporairement la vente en gros ?

**R:** Oui, deux options :
1. Changer la catégorie (de "business" à "mode" par exemple)
2. Mettre `quantite_minimale = 1`

---

### Q: Est-ce compatible avec les codes promo ?

**R:** Oui ! La quantité minimale est indépendante des réductions.

---

## 🎓 Conclusion

La fonctionnalité de quantité minimale est un **outil puissant** pour :

✅ Encourager les ventes en gros  
✅ Protéger vos marges  
✅ Filtrer les clients professionnels  
✅ Simplifier la gestion de stock  

**Utilisez-la avec discernement** pour maximiser son impact !

---

**Document créé pour Prestige Shop Express**  
*Version 1.0 - Mars 2026*
