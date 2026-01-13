-- =====================================================
-- MISE À JOUR TABLE UTILISATEURS - AJOUT DÉCONNEXION
-- =====================================================

-- Utilisation de la base de données existante
USE gestion_utilisateurs;

-- Ajout des colonnes pour la déconnexion
ALTER TABLE utilisateurs
ADD COLUMN session_active BOOLEAN DEFAULT FALSE,
ADD COLUMN token_session VARCHAR(255) NULL,
ADD COLUMN date_derniere_deconnexion TIMESTAMP NULL,
ADD COLUMN ip_derniere_deconnexion VARCHAR(45) NULL;

-- Création d'index pour les nouvelles colonnes
CREATE INDEX idx_session_active ON utilisateurs(session_active);
CREATE INDEX idx_token_session ON utilisateurs(token_session);

-- =====================================================
-- REQUÊTES POUR LA CONNEXION/DÉCONNEXION
-- =====================================================

-- 1. Connexion utilisateur (mettre à jour le statut de connexion)
-- UPDATE utilisateurs SET session_active = TRUE, token_session = 'abc123', derniere_connexion = NOW(), ip_connexion = '192.168.1.1' WHERE id = 1;

-- 2. Déconnexion utilisateur (mettre à jour le statut de déconnexion)
-- UPDATE utilisateurs SET session_active = FALSE, date_derniere_deconnexion = NOW(), ip_derniere_deconnexion = '192.168.1.1' WHERE token_session = 'abc123';

-- 3. Voir les utilisateurs actuellement connectés
-- SELECT * FROM utilisateurs WHERE session_active = TRUE;

-- 4. Voir l'historique des connexions (utilisateurs actifs récemment)
-- SELECT id, CONCAT(prenom, ' ', nom) as nom_complet, email, derniere_connexion, date_derniere_deconnexion FROM utilisateurs WHERE derniere_connexion IS NOT NULL ORDER BY derniere_connexion DESC;

-- 5. Déconnecter tous les utilisateurs (en cas de maintenance)
-- UPDATE utilisateurs SET session_active = FALSE, date_derniere_deconnexion = NOW();

-- 6. Vérifier si un utilisateur est connecté
-- SELECT session_active FROM utilisateurs WHERE id = 1;

-- =====================================================
-- PROCÉDURES POUR FACILITER LA GESTION
-- =====================================================

DELIMITER //

-- Procédure de connexion
CREATE PROCEDURE connecter_utilisateur(
    IN p_user_id INT,
    IN p_token VARCHAR(255),
    IN p_ip VARCHAR(45)
)
BEGIN
    UPDATE utilisateurs
    SET session_active = TRUE,
        token_session = p_token,
        derniere_connexion = NOW(),
        ip_connexion = p_ip
    WHERE id = p_user_id;
END //

-- Procédure de déconnexion
CREATE PROCEDURE deconnecter_utilisateur(
    IN p_token VARCHAR(255),
    IN p_ip VARCHAR(45)
)
BEGIN
    UPDATE utilisateurs
    SET session_active = FALSE,
        date_derniere_deconnexion = NOW(),
        ip_derniere_deconnexion = p_ip
    WHERE token_session = p_token;
END //

-- Procédure pour déconnecter un utilisateur par ID
CREATE PROCEDURE deconnecter_par_id(
    IN p_user_id INT,
    IN p_ip VARCHAR(45)
)
BEGIN
    UPDATE utilisateurs
    SET session_active = FALSE,
        date_derniere_deconnexion = NOW(),
        ip_derniere_deconnexion = p_ip
    WHERE id = p_user_id;
END //

DELIMITER ;

-- =====================================================
-- EXEMPLES D'UTILISATION DANS VOTRE CODE
-- =====================================================

-- Connexion :
-- CALL connecter_utilisateur(1, 'abc123xyz', '192.168.1.1');

-- Déconnexion avec token :
-- CALL deconnecter_utilisateur('abc123xyz', '192.168.1.1');

-- Déconnexion par ID utilisateur :
-- CALL deconnecter_par_id(1, '192.168.1.1');

-- Vérifier utilisateurs connectés :
-- SELECT COUNT(*) FROM utilisateurs WHERE session_active = TRUE;

-- Voir détails des connexions :
-- SELECT * FROM utilisateurs WHERE session_active = TRUE;
