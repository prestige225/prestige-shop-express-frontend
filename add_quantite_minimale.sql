-- Ajout de la colonne quantite_minimale pour la vente en gros (Prestige Business)
-- Cette colonne définit la quantité minimale d'achat pour les produits en gros

-- Vérifier si la colonne existe déjà
SET @dbname = DATABASE();
SET @tablename = 'produits';
SET @columnname = 'quantite_minimale';
SET @preparedStatement = (SELECT IF(
  (
    SELECT COUNT(*) FROM INFORMATION_SCHEMA.COLUMNS
    WHERE
      (table_name = @tablename)
      AND (table_schema = @dbname)
      AND (column_name = @columnname)
  ) > 0,
  'SELECT 1',
  CONCAT('ALTER TABLE ', @tablename, ' ADD COLUMN ', @columnname, ' INT DEFAULT 1 AFTER ordre')
));

PREPARE alterIfNotExists FROM @preparedStatement;
EXECUTE alterIfNotExists;
DEALLOCATE PREPARE alterIfNotExists;

-- Mettre à jour les produits existants de la catégorie "business" avec une valeur par défaut
UPDATE produits 
SET quantite_minimale = 5 
WHERE categorie = 'business' AND (quantite_minimale IS NULL OR quantite_minimale = 0);

-- Afficher un message de confirmation
SELECT '✅ Colonne quantite_minimale ajoutée/mise à jour avec succès !' as status;
