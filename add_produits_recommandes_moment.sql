-- =====================================================
-- Migration: Ajouter colonnes recommande et moment
-- =====================================================

-- Ajouter la colonne recommande (produit recommandé) si elle n'existe pas
ALTER TABLE produits ADD COLUMN IF NOT EXISTS recommande INT DEFAULT 0 COMMENT 'Produit recommandé (0 ou 1)';

-- Ajouter la colonne moment (produit du moment) si elle n'existe pas
ALTER TABLE produits ADD COLUMN IF NOT EXISTS moment INT DEFAULT 0 COMMENT 'Produit du moment (0 ou 1)';

-- Vérifier la structure de la table après les modifications
DESCRIBE produits;

-- Afficher les colonnes mises à jour
SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_DEFAULT, IS_NULLABLE 
FROM INFORMATION_SCHEMA.COLUMNS 
WHERE TABLE_NAME = 'produits' 
AND COLUMN_NAME IN ('recommande', 'moment')
ORDER BY ORDINAL_POSITION;