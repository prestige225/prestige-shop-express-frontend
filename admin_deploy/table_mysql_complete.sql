-- =====================================================
-- TABLE UTILISATEURS POUR LOGIN/REGISTER
-- Prestige Shop Express
-- =====================================================

-- Création de la base de données
CREATE DATABASE IF NOT EXISTS gestion_utilisateurs;

-- Utilisation de la base de données
USE gestion_utilisateurs;

-- Suppression de la table si elle existe déjà
DROP TABLE IF EXISTS utilisateurs;

-- Création de la table utilisateurs
CREATE TABLE utilisateurs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    mot_de_passe VARCHAR(255) NOT NULL,
    telephone VARCHAR(20),
    statut ENUM('actif', 'inactif', 'suspendu') DEFAULT 'actif',
    date_inscription TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    derniere_connexion TIMESTAMP NULL,
    ip_connexion VARCHAR(45),
    nombre_connexions INT DEFAULT 0,
    date_derniere_modification TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Index pour optimiser les performances
CREATE INDEX idx_email ON utilisateurs(email);
CREATE INDEX idx_statut ON utilisateurs(statut);
CREATE INDEX idx_date_inscription ON utilisateurs(date_inscription);
CREATE INDEX idx_derniere_connexion ON utilisateurs(derniere_connexion);

-- Insertion de quelques utilisateurs de test
INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, telephone, statut) VALUES
('Admin', 'Système', 'admin@prestigeshop.com', 'admin123', '0123456789', 'actif'),
('Dupont', 'Jean', 'jean.dupont@email.com', 'password123', '0111223344', 'actif'),
('Martin', 'Marie', 'marie.martin@email.com', 'password456', '0122334455', 'actif'),
('Dubois', 'Pierre', 'pierre.dubois@email.com', 'password789', '0133445566', 'inactif');

-- =====================================================
-- QUELQUES REQUÊTES UTILES
-- =====================================================

-- 1. Voir tous les utilisateurs inscrits
-- SELECT * FROM utilisateurs ORDER BY date_inscription DESC;

-- 2. Voir les utilisateurs actifs uniquement
-- SELECT * FROM utilisateurs WHERE statut = 'actif' ORDER BY derniere_connexion DESC;

-- 3. Voir qui s'est connecté aujourd'hui
-- SELECT * FROM utilisateurs WHERE DATE(derniere_connexion) = CURDATE() AND statut = 'actif';

-- 4. Compter le nombre d'utilisateurs actifs
-- SELECT COUNT(*) as total_actifs FROM utilisateurs WHERE statut = 'actif';

-- 5. Supprimer un utilisateur (mettre à jour le statut)
-- UPDATE utilisateurs SET statut = 'suspendu' WHERE id = 1;

-- 6. Supprimer définitivement un utilisateur
-- DELETE FROM utilisateurs WHERE id = 1;

-- 7. Enregistrer une connexion
-- UPDATE utilisateurs SET derniere_connexion = NOW(), ip_connexion = '192.168.1.1', nombre_connexions = nombre_connexions + 1 WHERE email = 'user@email.com';

-- =====================================================
-- PROCÉDURES STOCKÉES POUR FACILITER L'UTILISATION
-- =====================================================

DELIMITER //

-- Procédure pour créer un nouvel utilisateur (inscription)
CREATE PROCEDURE inscrire_utilisateur(
    IN p_nom VARCHAR(100),
    IN p_prenom VARCHAR(100),
    IN p_email VARCHAR(255),
    IN p_mot_de_passe VARCHAR(255),
    IN p_telephone VARCHAR(20)
)
BEGIN
    INSERT INTO utilisateurs (nom, prenom, email, mot_de_passe, telephone)
    VALUES (p_nom, p_prenom, p_email, p_mot_de_passe, p_telephone);
    SELECT LAST_INSERT_ID() as nouvel_id;
END //

-- Procédure pour vérifier les identifiants de connexion
CREATE PROCEDURE verifier_connexion(
    IN p_email VARCHAR(255),
    IN p_mot_de_passe VARCHAR(255)
)
BEGIN
    SELECT id, nom, prenom, email, statut
    FROM utilisateurs
    WHERE email = p_email
    AND mot_de_passe = p_mot_de_passe
    AND statut = 'actif';
END //

-- Procédure pour enregistrer une connexion réussie
CREATE PROCEDURE enregistrer_connexion(
    IN p_user_id INT,
    IN p_ip VARCHAR(45)
)
BEGIN
    UPDATE utilisateurs
    SET derniere_connexion = NOW(),
        ip_connexion = p_ip,
        nombre_connexions = nombre_connexions + 1
    WHERE id = p_user_id;
END //

-- Procédure pour suspendre un utilisateur
CREATE PROCEDURE suspendre_utilisateur(
    IN p_user_id INT
)
BEGIN
    UPDATE utilisateurs
    SET statut = 'suspendu'
    WHERE id = p_user_id;
END //

DELIMITER ;

-- =====================================================
-- VUES POUR FACILITER LES REQUÊTES
-- =====================================================

-- Vue des utilisateurs actifs
CREATE VIEW utilisateurs_actifs AS
SELECT id, CONCAT(prenom, ' ', nom) as nom_complet, email, derniere_connexion, nombre_connexions
FROM utilisateurs
WHERE statut = 'actif'
ORDER BY derniere_connexion DESC;

-- Vue des utilisateurs récemment connectés (24h)
CREATE VIEW connectes_aujourd_hui AS
SELECT id, CONCAT(prenom, ' ', nom) as nom_complet, email, derniere_connexion, ip_connexion
FROM utilisateurs
WHERE derniere_connexion >= DATE_SUB(NOW(), INTERVAL 24 HOUR)
AND statut = 'actif'
ORDER BY derniere_connexion DESC;

-- Vue des statistiques
CREATE VIEW statistiques AS
SELECT
    COUNT(*) as total_utilisateurs,
    SUM(CASE WHEN statut = 'actif' THEN 1 ELSE 0 END) as actifs,
    SUM(CASE WHEN statut = 'inactif' THEN 1 ELSE 0 END) as inactifs,
    SUM(CASE WHEN statut = 'suspendu' THEN 1 ELSE 0 END) as suspendus,
    SUM(CASE WHEN derniere_connexion >= DATE_SUB(NOW(), INTERVAL 24 HOUR) THEN 1 ELSE 0 END) as connectes_aujourd_hui,
    AVG(nombre_connexions) as connexions_moyennes
FROM utilisateurs;

-- =====================================================
-- EXEMPLES D'UTILISATION DANS VOTRE CODE PHP/JS
-- =====================================================

-- Inscription : CALL inscrire_utilisateur('Nom', 'Prénom', 'email@test.com', 'motdepasse', '0123456789');

-- Connexion : CALL verifier_connexion('email@test.com', 'motdepasse');

-- Enregistrer connexion : CALL enregistrer_connexion(1, '192.168.1.1');

-- Suspendre utilisateur : CALL suspendre_utilisateur(1);

-- Voir actifs : SELECT * FROM utilisateurs_actifs;

-- Voir connectés aujourd'hui : SELECT * FROM connectes_aujourd_hui;

-- Statistiques : SELECT * FROM statistiques;
