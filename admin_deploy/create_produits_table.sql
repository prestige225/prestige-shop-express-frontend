-- =====================================================
-- TABLE PRODUITS POUR PRESTIGE SHOP
-- =====================================================

-- Utilisation de la base de données
USE gestion_utilisateurs;

-- Création de la table produits
CREATE TABLE IF NOT EXISTS produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    prix DECIMAL(10, 2) NOT NULL,
    categorie VARCHAR(100),
    image_url VARCHAR(500),
    images_urls JSON,
    taille_disponible JSON,
    couleur_disponible JSON,
    stock INT DEFAULT 0,
    statut ENUM('actif', 'inactif', 'epuise') DEFAULT 'actif',
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Index pour optimiser les performances
CREATE INDEX idx_categorie ON produits(categorie);
CREATE INDEX idx_statut ON produits(statut);
CREATE INDEX idx_prix ON produits(prix);

-- Insertion de quelques produits de test
INSERT INTO produits (nom, description, prix, categorie, image_url, images_urls, stock, statut) VALUES
('T-shirt Prestige', 'T-shirt de qualité supérieure', 29.99, 'mode educatif', 'https://example.com/tshirt1.jpg', 
'["https://example.com/tshirt1.jpg", "https://example.com/tshirt2.jpg"]', 50, 'actif'),
('Casque Audio', 'Casque audio professionnel', 89.99, 'electronique', 'https://example.com/casque1.jpg', 
'["https://example.com/casque1.jpg", "https://example.com/casque2.jpg", "https://example.com/casque3.jpg"]', 20, 'actif'),
('Burger Gourmet', 'Burger fait maison avec ingrédients frais', 12.99, 'fast food', 'https://example.com/burger1.jpg', 
'["https://example.com/burger1.jpg", "https://example.com/burger2.jpg"]', 100, 'actif');

-- =====================================================
-- REQUÊTES UTILES POUR LES PRODUITS
-- =====================================================

-- 1. Voir tous les produits
-- SELECT * FROM produits;

-- 2. Voir les produits actifs seulement
-- SELECT * FROM produits WHERE statut = 'actif';

-- 3. Voir les produits par catégorie
-- SELECT * FROM produits WHERE categorie = 'electronique';

-- 4. Rechercher des produits par nom
-- SELECT * FROM produits WHERE nom LIKE '%T-shirt%';

-- 5. Mettre à jour le stock d'un produit
-- UPDATE produits SET stock = 45 WHERE id = 1;

-- 6. Mettre un produit comme épuisé
-- UPDATE produits SET statut = 'epuise' WHERE id = 1;

-- 7. Supprimer un produit
-- DELETE FROM produits WHERE id = 1;