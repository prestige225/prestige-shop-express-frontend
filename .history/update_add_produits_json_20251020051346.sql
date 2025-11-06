-- ========================================
-- Ajout de la colonne 'produits_json' pour stocker images et détails
-- ========================================

-- Ajouter la colonne produits_json (JSON complet avec images)
ALTER TABLE commandes
ADD COLUMN produits_json TEXT AFTER produits
COMMENT 'Détails complets des produits en JSON (nom, quantité, prix, image, description)';

-- Vérification
DESCRIBE commandes;

-- Exemple de contenu produits_json :
-- [{"nom":"iPhone 13","quantite":2,"prix":50000,"image":"https://...","description":"..."}]
