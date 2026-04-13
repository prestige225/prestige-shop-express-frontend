-- 🔧 FIX CRITIQUE: Correction de la quantite_minimale pour TOUS les produits Business
-- Le problème: Le script précédent (add_quantite_minimale.sql) ne check que 'business' 
-- Mais les vrais produits Business en BD ont 'categorie' = '💼 Prestige Business'
-- Cela explique pourquoi les nouveaux articles n'affichent pas le badge

-- 1️⃣ ÉTAPE 1: Vérifier quelles valeurs existent actuellement
SELECT DISTINCT categorie FROM produits ORDER BY categorie;

-- 2️⃣ ÉTAPE 2: Vérifier quels produits Business manquent une quantite_minimale correcte
SELECT id, nom, categorie, quantite_minimale 
FROM produits 
WHERE categorie = '💼 Prestige Business' 
OR categorie = 'Prestige Business'
OR categorie = 'business'
ORDER BY id DESC;

-- 3️⃣ ÉTAPE 3: CORRECTION - Mettre à jour TOUS les produits Business avec quantité minimale
UPDATE produits 
SET quantite_minimale = 3 
WHERE (
    categorie = '💼 Prestige Business' 
    OR categorie = 'Prestige Business'
    OR categorie = 'business'
    OR categorie LIKE '%Prestige Business%'
)
AND (quantite_minimale IS NULL OR quantite_minimale <= 1);

-- 4️⃣ ÉTAPE 4: Vérifier que la correction a fonctionné
SELECT id, nom, categorie, quantite_minimale 
FROM produits 
WHERE categorie LIKE '%Prestige Business%'
OR categorie = 'business'
ORDER BY id DESC;

-- 5️⃣ ÉTAPE 5: Compter les produits Business maintenant correctement configurés
SELECT 
    COUNT(*) as total_business,
    SUM(CASE WHEN quantite_minimale >= 3 THEN 1 ELSE 0 END) as with_correct_qty,
    SUM(CASE WHEN quantite_minimale IS NULL OR quantite_minimale <= 1 THEN 1 ELSE 0 END) as still_broken
FROM produits 
WHERE categorie LIKE '%Prestige Business%'
OR categorie = 'business';
