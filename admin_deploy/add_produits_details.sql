-- Ajouter colonne pour stocker les détails complets des produits (avec images)
ALTER TABLE commandes
ADD COLUMN produits_details JSON
COMMENT 'Détails complets: nom, quantité, prix, image';

-- Vérification
DESCRIBE commandes;
