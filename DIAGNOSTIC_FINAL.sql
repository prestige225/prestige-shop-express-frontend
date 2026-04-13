-- 🔧 DIAGNOSTIC FINAL - Pourquoi les 8 articles n'affichent pas?

-- 1️⃣ Chercher TOUS les articles avec "Business" dans la catégorie
SELECT 
    id,
    nom,
    categorie,
    quantite_minimale,
    statut,
    stock,
    CONCAT(
        CASE 
            WHEN statut != 'actif' THEN '❌ STATUT INACTIF: ' || statut || ' | '
            ELSE '✓ Actif | '
        END,
        CASE 
            WHEN quantite_minimale IS NULL THEN '❌ quantite_minimale = NULL | '
            WHEN quantite_minimale <= 1 THEN '❌ quantite_minimale = ' || quantite_minimale || ' (trop bas) | '
            ELSE '✓ quantite_minimale = ' || quantite_minimale || ' | '
        END,
        CASE 
            WHEN stock <= 0 THEN '❌ STOCK=0 | '
            ELSE '✓ Stock OK | '
        END
    ) as diagnostique
FROM produits
WHERE categorie LIKE '%Business%'
   OR categorie LIKE '%business%'
ORDER BY id DESC;

-- 2️⃣ Compter combien devraient VRAIMENT afficher le badge
SELECT 
    COUNT(*) as total_business,
    SUM(CASE WHEN statut = 'actif' AND quantite_minimale > 1 AND stock > 0 THEN 1 ELSE 0 END) as devraient_afficher,
    SUM(CASE WHEN statut != 'actif' THEN 1 ELSE 0 END) as inactifs_ou_rupture,
    SUM(CASE WHEN quantite_minimale <= 1 THEN 1 ELSE 0 END) as sans_quantite_minimale
FROM produits
WHERE categorie LIKE '%Business%'
   OR categorie LIKE '%business%';

-- 3️⃣ Si moins de 8 affichent le badge, utiliser cette requête pour les CORRIGER:
/*
UPDATE produits
SET quantite_minimale = 3
WHERE (categorie LIKE '%Business%' OR categorie LIKE '%business%')
  AND (quantite_minimale IS NULL OR quantite_minimale <= 1)
  AND statut = 'actif';
*/
