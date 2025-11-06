-- =====================================================
-- MISE À JOUR DE LA TABLE PRODUITS - AJOUT SUPPORT VIDÉOS
-- =====================================================

-- Utilisation de la base de données
USE bracv1wswmu4vsqxycku;

-- Ajout de la colonne videos_urls si elle n'existe pas déjà
ALTER TABLE produits 
ADD COLUMN IF NOT EXISTS videos_urls JSON AFTER images_urls;

-- Vérification de la structure mise à jour
DESCRIBE produits;

-- Mise à jour des produits existants pour ajouter un tableau vide de vidéos si nécessaire
UPDATE produits 
SET videos_urls = '[]' 
WHERE videos_urls IS NULL;

-- Exemple d'insertion de produit avec vidéos (si vous voulez en ajouter)
-- INSERT INTO produits (nom, description, prix, categorie, image_url, images_urls, videos_urls, stock, statut) VALUES
-- ('Exemple Produit', 'Description du produit', 29.99, 'electronique', 'https://example.com/image1.jpg', 
-- '["https://example.com/image1.jpg", "https://example.com/image2.jpg"]', '["https://example.com/video1.mp4"]', 10, 'actif');