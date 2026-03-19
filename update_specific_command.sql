-- ========================================
-- Mise à jour manuelle d'une commande spécifique
-- ========================================

-- Pour la commande CMD-20260319-4063 (exemple)
-- Remplacez '0707070707' par le vrai numéro de téléphone

UPDATE commandes 
SET telephone = '0707070707'  -- ⚠️ REMPLACEZ PAR LE VRAI NUMÉRO
WHERE numero_commande = 'CMD-20260319-4063';

-- Vérifier la mise à jour
SELECT 
    id,
    numero_commande,
    user_id,
    telephone,
    nom,
    email,
    adresse_livraison
FROM commandes c
LEFT JOIN users u ON c.user_id = u.id
WHERE numero_commande = 'CMD-20260319-4063';
