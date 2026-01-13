-- ========================================
-- Ajout de la colonne 'produits' à la table commandes
-- ========================================
-- Cette colonne stockera les noms des produits achetés
-- Format: "Produit1 (x2), Produit2 (x1), Produit3 (x3)"

-- Vérifier d'abord si la colonne existe déjà
-- Si elle n'existe pas, l'ajouter

ALTER TABLE commandes
ADD COLUMN produits TEXT AFTER telephone;

-- Ajouter un commentaire pour documenter la colonne
ALTER TABLE commandes
MODIFY COLUMN produits TEXT COMMENT 'Liste des produits commandés au format: Nom (xQuantité), Nom2 (xQuantité2)';

-- ========================================
-- Mettre à jour les commandes existantes
-- ========================================
-- Extraire les produits depuis la colonne 'notes' pour les anciennes commandes

UPDATE commandes
SET produits = SUBSTRING_INDEX(SUBSTRING_INDEX(notes, 'Produits: ', -1), ' - ', 1)
WHERE notes LIKE '%Produits:%' AND (produits IS NULL OR produits = '');

-- ========================================
-- Vérification
-- ========================================
-- Afficher les 5 dernières commandes avec les produits

SELECT 
    id,
    numero_commande,
    produits,
    montant_total,
    statut,
    date_commande
FROM commandes
ORDER BY date_commande DESC
LIMIT 5;
