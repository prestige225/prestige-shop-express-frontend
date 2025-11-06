-- =====================================================
-- TABLE UTILISATEURS SIMPLE - PRESTIGE SHOP
-- =====================================================

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS users_db;

-- Utilisation de la base de données
USE users_db;

-- Table utilisateurs simple
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    statut VARCHAR(20) DEFAULT 'actif',
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    derniere_connexion TIMESTAMP NULL
);

-- Index simples
CREATE INDEX idx_email ON users(email);
CREATE INDEX idx_statut ON users(statut);

-- Utilisateurs de test
INSERT INTO users (nom, prenom, email, mot_de_passe) VALUES
('Admin', 'Système', 'admin@test.com', 'admin123'),
('Dupont', 'Jean', 'jean@test.com', 'password123'),
('Martin', 'Marie', 'marie@test.com', 'password456');

-- =====================================================
-- REQUÊTES SIMPLES À UTILISER
-- =====================================================

-- 1. Voir tous les utilisateurs inscrits
-- SELECT * FROM users;

-- 2. Voir seulement les utilisateurs actifs
-- SELECT * FROM users WHERE statut = 'actif';

-- 3. Voir les utilisateurs connectés aujourd'hui
-- SELECT * FROM users WHERE DATE(derniere_connexion) = CURDATE();

-- 4. Supprimer un utilisateur
-- DELETE FROM users WHERE id = 1;

-- 5. Suspendre un utilisateur
-- UPDATE users SET statut = 'suspendu' WHERE id = 1;

-- 6. Enregistrer une connexion
-- UPDATE users SET derniere_connexion = NOW() WHERE id = 1;
