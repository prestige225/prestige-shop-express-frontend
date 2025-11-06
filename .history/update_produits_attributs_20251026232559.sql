-- =====================================================
-- MISE À JOUR DE LA BASE DE DONNÉES POUR LES ATTRIBUTS DE PRODUITS
-- Prestige Shop Express
-- =====================================================

-- Création de la table pour les attributs de produits
CREATE TABLE IF NOT EXISTS produit_attributs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    produit_id INT NOT NULL,
    couleur VARCHAR(50),
    taille VARCHAR(20),
    stock INT DEFAULT 0,
    prix_additionnel DECIMAL(10,2) DEFAULT 0.00,
    image_url VARCHAR(500),
    date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    date_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (produit_id) REFERENCES commandes(id) ON DELETE CASCADE
);

-- Ajout d'index pour améliorer les performances
CREATE INDEX idx_produit_id ON produit_attributs(produit_id);
CREATE INDEX idx_couleur ON produit_attributs(couleur);
CREATE INDEX idx_taille ON produit_attributs(taille);

-- Insertion d'exemples d'attributs pour des baskets
INSERT INTO produit_attributs (produit_id, couleur, taille, stock, prix_additionnel, image_url) VALUES
-- Baskets Adidas Tendance Noir & Rose (produit id 9)
(9, 'Noir/Rose', '36', 5, 0.00, 'imageprestige/adg.jpg'),
(9, 'Noir/Rose', '37', 3, 0.00, 'imageprestige/adg.jpg'),
(9, 'Noir/Rose', '38', 7, 0.00, 'imageprestige/adg.jpg'),
(9, 'Noir/Rose', '39', 4, 0.00, 'imageprestige/adg.jpg'),
(9, 'Noir/Rose', '40', 6, 0.00, 'imageprestige/adg.jpg'),
(9, 'Noir/Rose', '41', 2, 0.00, 'imageprestige/adg.jpg'),
(9, 'Noir/Rose', '42', 1, 0.00, 'imageprestige/adg.jpg'),

-- Baskets Rétro Élégantes (produit id 10)
(10, 'Blanc/Bleu', '36', 4, 0.00, 'imageprestige/AE86.jpg'),
(10, 'Blanc/Bleu', '37', 5, 0.00, 'imageprestige/AE86.jpg'),
(10, 'Blanc/Bleu', '38', 6, 0.00, 'imageprestige/AE86.jpg'),
(10, 'Blanc/Bleu', '39', 3, 0.00, 'imageprestige/AE86.jpg'),
(10, 'Blanc/Bleu', '40', 5, 0.00, 'imageprestige/AE86.jpg'),
(10, 'Blanc/Bleu', '41', 2, 0.00, 'imageprestige/AE86.jpg'),
(10, 'Blanc/Bleu', '42', 1, 0.00, 'imageprestige/AE86.jpg'),

-- Baskets Hautes Élégance Poudrée (produit id 11)
(11, 'Bleu/Rose', '35', 3, 0.00, 'imageprestige/airf.jpg'),
(11, 'Bleu/Rose', '36', 5, 0.00, 'imageprestige/airf.jpg'),
(11, 'Bleu/Rose', '37', 4, 0.00, 'imageprestige/airf.jpg'),
(11, 'Bleu/Rose', '38', 6, 0.00, 'imageprestige/airf.jpg'),
(11, 'Bleu/Rose', '39', 3, 0.00, 'imageprestige/airf.jpg'),
(11, 'Bleu/Rose', '40', 2, 0.00, 'imageprestige/airf.jpg'),
(11, 'Bleu/Rose', '41', 1, 0.00, 'imageprestige/airf.jpg'),

-- Baskets Blanches Pures (produit id 12)
(12, 'Blanc', '36', 6, 0.00, 'imageprestige/airh.jpg'),
(12, 'Blanc', '37', 5, 0.00, 'imageprestige/airh.jpg'),
(12, 'Blanc', '38', 7, 0.00, 'imageprestige/airh.jpg'),
(12, 'Blanc', '39', 4, 0.00, 'imageprestige/airh.jpg'),
(12, 'Blanc', '40', 5, 0.00, 'imageprestige/airh.jpg'),
(12, 'Blanc', '41', 3, 0.00, 'imageprestige/airh.jpg'),
(12, 'Blanc', '42', 2, 0.00, 'imageprestige/airh.jpg');

-- Création d'une vue pour obtenir facilement les informations des produits avec leurs attributs
CREATE OR REPLACE VIEW vue_produits_complets AS
SELECT 
    p.id as produit_id,
    p.name as nom_produit,
    p.price as prix_base,
    p.category as categorie,
    p.subcategory as sous_categorie,
    p.images,
    p.description,
    pa.id as attribut_id,
    pa.couleur,
    pa.taille,
    pa.stock,
    (p.price + pa.prix_additionnel) as prix_final,
    pa.image_url
FROM commandes p
LEFT JOIN produit_attributs pa ON p.id = pa.produit_id
ORDER BY p.id, pa.couleur, pa.taille;

-- =====================================================
-- REQUÊTES UTILES
-- =====================================================

-- 1. Voir tous les attributs d'un produit spécifique
-- SELECT * FROM produit_attributs WHERE produit_id = 9;

-- 2. Voir les tailles disponibles pour un produit et une couleur
-- SELECT DISTINCT taille FROM produit_attributs WHERE produit_id = 9 AND couleur = 'Noir/Rose' AND stock > 0;

-- 3. Voir les couleurs disponibles pour un produit et une taille
-- SELECT DISTINCT couleur FROM produit_attributs WHERE produit_id = 9 AND taille = '38' AND stock > 0;

-- 4. Vérifier le stock pour un attribut spécifique
-- SELECT stock FROM produit_attributs WHERE produit_id = 9 AND couleur = 'Noir/Rose' AND taille = '38';

-- 5. Voir tous les produits avec leurs attributs
-- SELECT * FROM vue_produits_complets;

-- =====================================================
-- FONCTIONS STOCK
-- =====================================================

DELIMITER //

-- Fonction pour vérifier si un produit est disponible dans une taille et couleur spécifiques
CREATE FUNCTION verifier_disponibilite(produit_id INT, couleur_choisie VARCHAR(50), taille_choisie VARCHAR(20))
RETURNS BOOLEAN
READS SQL DATA
DETERMINISTIC
BEGIN
    DECLARE disponible BOOLEAN DEFAULT FALSE;
    DECLARE stock_dispo INT;
    
    SELECT stock INTO stock_dispo
    FROM produit_attributs
    WHERE produit_id = produit_id 
    AND couleur = couleur_choisie 
    AND taille = taille_choisie
    LIMIT 1;
    
    IF stock_dispo > 0 THEN
        SET disponible = TRUE;
    END IF;
    
    RETURN disponible;
END //

-- Procédure pour mettre à jour le stock après une commande
CREATE PROCEDURE mettre_a_jour_stock(
    IN produit_id INT,
    IN couleur_choisie VARCHAR(50),
    IN taille_choisie VARCHAR(20),
    IN quantite_vendue INT
)
BEGIN
    UPDATE produit_attributs
    SET stock = stock - quantite_vendue
    WHERE produit_id = produit_id 
    AND couleur = couleur_choisie 
    AND taille = taille_choisie;
END //

DELIMITER ;

-- =====================================================
-- EXEMPLES D'UTILISATION
-- =====================================================

-- Vérifier la disponibilité d'une basket noir/rose en taille 38:
-- SELECT verifier_disponibilite(9, 'Noir/Rose', '38') as disponible;

-- Mettre à jour le stock après une vente de 2 paires de baskets noir/rose taille 38:
-- CALL mettre_a_jour_stock(9, 'Noir/Rose', '38', 2);