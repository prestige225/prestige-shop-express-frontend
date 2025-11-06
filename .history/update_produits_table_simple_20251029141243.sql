-- =====================================================
-- MISE À JOUR DE LA TABLE PRODUITS - AJOUT SUPPORT VIDÉOS
-- =====================================================

-- Ajout de la colonne videos_urls si elle n'existe pas déjà
ALTER TABLE produits 
ADD COLUMN IF NOT EXISTS videos_urls JSON AFTER images_urls;

-- Vérification de la structure mise à jour
DESCRIBE produits;

-- Mise à jour des produits existants pour ajouter un tableau vide de vidéos si nécessaire
UPDATE produits 
SET videos_urls = '[]' 
WHERE videos_urls IS NULL;