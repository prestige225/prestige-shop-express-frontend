-- =====================================================
-- MISE À JOUR DE LA TABLE PRODUITS - AJOUT DE LA COLONNE VIDEOS_URLS
-- =====================================================

-- Utilisation de la base de données
USE bracv1wswmu4vsqxycku;

-- Ajout de la colonne videos_urls à la table produits
ALTER TABLE produits
ADD COLUMN videos_urls JSON
COMMENT 'URLs des vidéos du produit (format JSON array)';

-- Vérification de la structure de la table
DESCRIBE produits;

-- Mise à jour d'un produit existant pour tester la nouvelle colonne
UPDATE produits 
SET videos_urls = JSON_ARRAY('https://example.com/video1.mp4', 'https://example.com/video2.mp4') 
WHERE id = 1;

-- Vérification des données
SELECT id, nom, videos_urls FROM produits WHERE id = 1;