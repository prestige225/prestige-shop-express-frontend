-- =====================================================
-- TABLE PRODUITS POUR PRESTIGE SHOP EXPRESS
-- =====================================================

USE gestion_utilisateurs;

-- Suppression de la table si elle existe déjà
DROP TABLE IF EXISTS produits;

-- Création de la table produits
CREATE TABLE produits (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    description TEXT,
    prix DECIMAL(10, 2) NOT NULL,
    categorie VARCHAR(100),
    image_url VARCHAR(500),
    images_urls JSON, -- Pour stocker plusieurs images
    taille_disponible JSON, -- Ex: ["S", "M", "L", "XL"]
    couleur_disponible JSON, -- Ex: ["Rouge", "Bleu", "Vert"]
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
INSERT INTO produits (nom, description, prix, categorie, image_url, images_urls, taille_disponible, couleur_disponible, stock) VALUES
('Chaussures de sport', 'Chaussures de sport confortables pour hommes, idéales pour la course à pied et le fitness.', 89.99, 'Chaussures', 'images/chaussures_sport.jpg', 
'["images/chaussures_sport_1.jpg", "images/chaussures_sport_2.jpg", "images/chaussures_sport_3.jpg"]', 
'["39", "40", "41", "42", "43", "44"]', 
'["Noir", "Blanc", "Bleu"]', 50),

('T-shirt en coton', 'T-shirt 100% coton, respirant et confortable pour un usage quotidien.', 24.99, 'Vêtements', 'images/tshirt.jpg',
'["images/tshirt_1.jpg", "images/tshirt_2.jpg"]',
'["S", "M", "L", "XL", "XXL"]',
'["Rouge", "Bleu", "Vert", "Noir"]', 100),

('Sac à dos étudiant', 'Sac à dos spacieux avec plusieurs compartiments, idéal pour l\'école ou le travail.', 59.99, 'Accessoires', 'images/sac_a_dos.jpg',
'["images/sac_a_dos_1.jpg", "images/sac_a_dos_2.jpg", "images/sac_a_dos_3.jpg"]',
'[]',
'["Noir", "Gris", "Bleu"]', 30),

('Montre connectée', 'Montre intelligente avec suivi d\'activité, notifications et autonomie de 7 jours.', 129.99, 'Électronique', 'images/montre_connectee.jpg',
'["images/montre_connectee_1.jpg", "images/montre_connectee_2.jpg"]',
'[]',
'["Noir", "Argent", "Or"]', 25),

('Casque audio sans fil', 'Casque Bluetooth avec réduction de bruit active et qualité sonore exceptionnelle.', 149.99, 'Électronique', 'images/casque_audio.jpg',
'["images/casque_audio_1.jpg", "images/casque_audio_2.jpg", "images/casque_audio_3.jpg"]',
'[]',
'["Noir", "Blanc", "Rouge"]', 40);

-- =====================================================
-- REQUÊTES UTILES POUR LES PRODUITS
-- =====================================================

-- 1. Voir tous les produits actifs
-- SELECT * FROM produits WHERE statut = 'actif' ORDER BY date_creation DESC;

-- 2. Voir les produits par catégorie
-- SELECT * FROM produits WHERE categorie = 'Chaussures' AND statut = 'actif';

-- 3. Rechercher des produits par nom
-- SELECT * FROM produits WHERE nom LIKE '%chaussures%' AND statut = 'actif';

-- 4. Voir les produits en rupture de stock
-- SELECT * FROM produits WHERE stock = 0 AND statut = 'actif';

-- 5. Mettre à jour le stock d'un produit
-- UPDATE produits SET stock = stock - 1 WHERE id = 1;

-- 6. Mettre un produit en rupture
-- UPDATE produits SET statut = 'epuise' WHERE stock = 0;
