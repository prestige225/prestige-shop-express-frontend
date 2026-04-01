-- ============================================
-- Script SQL: Mettre un produit en rupture de stock
-- ============================================

-- Option 1: Mettre à jour un produit spécifique (remplacez 147 par l'ID souhaité)
UPDATE produits 
SET statut = 'epuise',
    date_mise_a_jour = NOW()
WHERE id = 147;

-- Vérification
SELECT id, nom, prix, stock, statut, date_mise_a_jour
FROM produits 
WHERE id = 147;

-- ============================================
-- Option 2: Mettre plusieurs produits en rupture
-- ============================================
/*
UPDATE produits 
SET statut = 'epuise',
    date_mise_a_jour = NOW()
WHERE id IN (147, 148, 149);
*/

-- ============================================
-- Option 3: Voir tous les produits épuisés
-- ============================================
/*
SELECT 
    id, 
    nom, 
    prix, 
    stock, 
    statut,
    date_mise_a_jour
FROM produits 
WHERE statut = 'epuise'
ORDER BY date_mise_a_jour DESC;
*/

-- ============================================
-- Option 4: Compter les produits par statut
-- ============================================
/*
SELECT 
    statut,
    COUNT(*) as nombre,
    GROUP_CONCAT(nom SEPARATOR ', ') as produits
FROM produits
GROUP BY statut;
*/
