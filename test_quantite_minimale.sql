-- ============================================
-- TEST DE LA FONCTIONNALITÉ QUANTITÉ MINIMALE
-- ============================================

-- 1️⃣ VÉRIFIER que la colonne existe
SELECT 
    COLUMN_NAME, 
    DATA_TYPE, 
    COLUMN_DEFAULT,
    IS_NULLABLE
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_SCHEMA = DATABASE()
  AND TABLE_NAME = 'produits'
  AND COLUMN_NAME = 'quantite_minimale';

-- 2️⃣ VOIR tous les produits Prestige Business avec leur quantité minimale
SELECT 
    id,
    nom,
    categorie,
    sous_categorie,
    prix,
    quantite_minimale,
    stock,
    statut
FROM produits
WHERE categorie = 'business'
ORDER BY quantite_minimale DESC, nom ASC;

-- 3️⃣ STATISTIQUES par catégorie
SELECT 
    categorie,
    COUNT(*) as nombre_produits,
    AVG(quantite_minimale) as quantite_minimale_moyenne,
    MIN(quantite_minimale) as min_absolu,
    MAX(quantite_minimale) as max_absolu
FROM produits
GROUP BY categorie
ORDER BY categorie;

-- 4️⃣ PRODUITS AVEC LA PLUS FORTE QUANTITÉ MINIMALE
SELECT 
    id,
    nom,
    categorie,
    prix,
    quantite_minimale,
    CONCAT(
        'Valeur totale minimum: ',
        FORMAT(prix * quantite_minimale, 0, 'fr_FR'),
        ' FCFA'
    ) as valeur_minimum_commande
FROM produits
WHERE quantite_minimale >= 10
ORDER BY quantite_minimale DESC
LIMIT 10;

-- 5️⃣ VÉRIFIER LES PRODUITS SANS QUANTITÉ MINIMALE (doivent être à 1 par défaut)
SELECT 
    id,
    nom,
    categorie,
    CASE 
        WHEN quantite_minimale IS NULL THEN '❌ NULL'
        WHEN quantite_minimale = 0 THEN '❌ ZÉRO'
        WHEN quantite_minimale = 1 THEN '✅ DÉFAUT (1)'
        ELSE CONCAT('✅ PERSONNISÉ (', quantite_minimale, ')')
    END as statut_quantite
FROM produits
WHERE quantite_minimale IS NULL OR quantite_minimale <= 1
ORDER BY id DESC
LIMIT 20;

-- 6️⃣ MISE À JOUR MANUELLE (si besoin)
-- Pour modifier la quantité minimale d'un produit spécifique :
/*
UPDATE produits 
SET quantite_minimale = 20 
WHERE id = VOTRE_ID_ICI;
*/

-- 7️⃣ EXEMPLES DE MISES À JOUR EN MASSE
/*
-- Tous les produits business à 10 unités minimum
UPDATE produits 
SET quantite_minimale = 10 
WHERE categorie = 'business';

-- Produits électronique à 5 unités
UPDATE produits 
SET quantite_minimale = 5 
WHERE categorie = 'electronique';

-- Remise à 1 pour tous les autres
UPDATE produits 
SET quantite_minimale = 1 
WHERE categorie NOT IN ('business');
*/

-- 8️⃣ RÉSULTAT FINAL ATTENDU
SELECT 
    '✅ Installation réussie !' as status,
    (SELECT COUNT(*) FROM produits WHERE quantite_minimale IS NOT NULL) as produits_avec_quantite,
    (SELECT COUNT(*) FROM produits WHERE categorie = 'business' AND quantite_minimale >= 5) as business_valides;
