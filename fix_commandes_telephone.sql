-- ========================================
-- Script pour récupérer les téléphones manquants des commandes
-- ========================================

-- 1. Identifier les commandes sans téléphone
SELECT 
    c.id,
    c.numero_commande,
    c.user_id,
    c.telephone,
    u.nom,
    u.prenom,
    u.telephone as user_telephone,
    c.notes
FROM commandes c
LEFT JOIN users u ON c.user_id = u.id
WHERE c.telephone IS NULL OR c.telephone = ''
ORDER BY c.date_commande DESC;

-- 2. Mettre à jour les commandes avec le téléphone de l'utilisateur (si disponible)
UPDATE commandes c
INNER JOIN users u ON c.user_id = u.id
SET c.telephone = u.telephone
WHERE (c.telephone IS NULL OR c.telephone = '')
  AND (u.telephone IS NOT NULL AND u.telephone != '');

-- 3. Vérifier les commandes toujours sans téléphone après mise à jour
SELECT 
    c.id,
    c.numero_commande,
    c.user_id,
    c.telephone,
    u.nom,
    u.prenom,
    u.telephone as user_telephone,
    c.notes
FROM commandes c
LEFT JOIN users u ON c.user_id = u.id
WHERE c.telephone IS NULL OR c.telephone = ''
ORDER BY c.date_commande DESC;

-- 4. Statistiques avant/après
SELECT 
    COUNT(*) as total_commandes,
    SUM(CASE WHEN telephone IS NULL OR telephone = '' THEN 1 ELSE 0 END) as sans_telephone,
    SUM(CASE WHEN telephone IS NOT NULL AND telephone != '' THEN 1 ELSE 0 END) as avec_telephone
FROM commandes;
