-- ========================================
-- ÉTAPE 1: Ajouter la colonne 'produits' (EXÉCUTER EN PREMIER)
-- ========================================

-- Vérifier si la colonne existe avant de l'ajouter
-- MySQL ne supporte pas IF EXISTS pour ADD COLUMN, donc on utilise une procédure

DELIMITER $$

CREATE PROCEDURE AddProduitsColumn()
BEGIN
    -- Vérifier si la colonne existe déjà
    IF NOT EXISTS (
        SELECT * FROM information_schema.COLUMNS 
        WHERE TABLE_SCHEMA = 'bracv1wswmu4vsqxycku' 
        AND TABLE_NAME = 'commandes' 
        AND COLUMN_NAME = 'produits'
    ) THEN
        -- Ajouter la colonne si elle n'existe pas
        ALTER TABLE commandes ADD COLUMN produits TEXT AFTER telephone;
        SELECT 'Colonne produits ajoutée avec succès' AS Message;
    ELSE
        SELECT 'La colonne produits existe déjà' AS Message;
    END IF;
END$$

DELIMITER ;

-- Exécuter la procédure
CALL AddProduitsColumn();

-- Supprimer la procédure après utilisation
DROP PROCEDURE IF EXISTS AddProduitsColumn;

-- ========================================
-- ÉTAPE 2: Mettre à jour les commandes existantes
-- ========================================

-- Extraire les produits depuis 'notes' pour les anciennes commandes
UPDATE commandes
SET produits = SUBSTRING_INDEX(SUBSTRING_INDEX(notes, 'Produits: ', -1), ' - ', 1)
WHERE notes LIKE '%Produits:%' 
  AND (produits IS NULL OR produits = '');

-- ========================================
-- ÉTAPE 3: Vérification
-- ========================================

-- Vérifier la structure de la table
DESCRIBE commandes;

-- Afficher les 5 dernières commandes avec les produits
SELECT 
    id,
    numero_commande,
    produits,
    montant_total,
    statut,
    DATE_FORMAT(date_commande, '%d/%m/%Y %H:%i') as date
FROM commandes
ORDER BY date_commande DESC
LIMIT 5;

-- Compter les commandes avec produits
SELECT 
    COUNT(*) as total_commandes,
    SUM(CASE WHEN produits IS NOT NULL AND produits != '' THEN 1 ELSE 0 END) as avec_produits,
    SUM(CASE WHEN produits IS NULL OR produits = '' THEN 1 ELSE 0 END) as sans_produits
FROM commandes;
