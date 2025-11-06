-- Migration: ajouter la colonne videos_urls (JSON) à la table produits
-- Emplacement: migrations/add_videos_urls_to_produits.sql
-- Exécuter cette commande SQL sur votre base MySQL pour ajouter la colonne :

ALTER TABLE produits
ADD COLUMN videos_urls JSON NULL AFTER images_urls;

-- Vérifier ensuite que la colonne a bien été ajoutée :
-- DESCRIBE produits;
