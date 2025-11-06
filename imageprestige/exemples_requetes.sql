-- =====================================================
-- REQUÊTES PRATIQUES POUR VOTRE TABLE USERS
-- =====================================================

USE gestion_utilisateurs;

-- =====================================================
-- 1. CONNEXION D'UTILISATEURS
-- =====================================================

-- Connecter l'admin (id = 1)
UPDATE users SET session_active = 1, token_session = 'admin_token_123', derniere_connexion = NOW(), ip_connexion = '192.168.1.100' WHERE id = 1;

-- Connecter Jean Dupont (id = 2)
UPDATE users SET session_active = 1, token_session = 'jean_token_456', derniere_connexion = NOW(), ip_connexion = '192.168.1.101' WHERE id = 2;

-- Connecter Marie Martin (id = 3)
UPDATE users SET session_active = 1, token_session = 'marie_token_789', derniere_connexion = NOW(), ip_connexion = '192.168.1.102' WHERE id = 3;

-- =====================================================
-- 2. VOIR LES UTILISATEURS CONNECTÉS
-- =====================================================

-- Voir tous les utilisateurs avec leur statut de connexion
SELECT
    id,
    CONCAT(prenom, ' ', nom) as nom_complet,
    email,
    statut,
    CASE WHEN session_active = 1 THEN 'CONNECTÉ' ELSE 'DÉCONNECTÉ' END as statut_connexion,
    derniere_connexion,
    token_session
FROM users
ORDER BY derniere_connexion DESC;

-- Voir seulement les utilisateurs actuellement connectés
SELECT
    id,
    CONCAT(prenom, ' ', nom) as nom_complet,
    email,
    derniere_connexion,
    ip_connexion,
    token_session
FROM users
WHERE session_active = 1;

-- Compter le nombre d'utilisateurs connectés
SELECT COUNT(*) as utilisateurs_connectes FROM users WHERE session_active = 1;

-- =====================================================
-- 3. DÉCONNEXION D'UTILISATEURS
-- =====================================================

-- Déconnecter l'admin avec son token
UPDATE users
SET session_active = 0,
    date_derniere_deconnexion = NOW(),
    ip_derniere_deconnexion = '192.168.1.100'
WHERE token_session = 'admin_token_123';

-- Déconnecter Jean Dupont avec son token
UPDATE users
SET session_active = 0,
    date_derniere_deconnexion = NOW(),
    ip_derniere_deconnexion = '192.168.1.101'
WHERE token_session = 'jean_token_456';

-- Déconnecter par ID utilisateur (si pas de token)
UPDATE users
SET session_active = 0,
    date_derniere_deconnexion = NOW(),
    ip_derniere_deconnexion = '192.168.1.102'
WHERE id = 3;

-- =====================================================
-- 4. HISTORIQUE DES CONNEXIONS
-- =====================================================

-- Voir l'historique complet des connexions et déconnexions
SELECT
    id,
    CONCAT(prenom, ' ', nom) as nom_complet,
    email,
    derniere_connexion,
    date_derniere_deconnexion,
    ip_connexion,
    ip_derniere_deconnexion,
    CASE WHEN session_active = 1 THEN 'Actuellement connecté' ELSE 'Déconnecté' END as statut_actuel
FROM users
WHERE derniere_connexion IS NOT NULL
ORDER BY derniere_connexion DESC;

-- =====================================================
-- 5. SUPPRESSION ET GESTION DES UTILISATEURS
-- =====================================================

-- Suspendre un utilisateur (au lieu de supprimer définitivement)
UPDATE users SET statut = 'suspendu' WHERE id = 1;

-- Réactiver un utilisateur suspendu
UPDATE users SET statut = 'actif' WHERE id = 1;

-- Supprimer définitivement un utilisateur
DELETE FROM users WHERE id = 1;

-- Voir seulement les utilisateurs actifs
SELECT * FROM users WHERE statut = 'actif';

-- Voir les utilisateurs suspendus
SELECT * FROM users WHERE statut = 'suspendu';

-- =====================================================
-- 6. STATISTIQUES RAPIDES
-- =====================================================

-- Nombre total d'utilisateurs
SELECT COUNT(*) as total_utilisateurs FROM users;

-- Nombre d'utilisateurs actifs
SELECT COUNT(*) as utilisateurs_actifs FROM users WHERE statut = 'actif';

-- Nombre d'utilisateurs connectés en ce moment
SELECT COUNT(*) as connectes_maintenant FROM users WHERE session_active = 1;

-- Nombre d'utilisateurs connectés aujourd'hui
SELECT COUNT(*) as connectes_aujourdhui FROM users WHERE DATE(derniere_connexion) = CURDATE();

-- =====================================================
-- 7. RÉINITIALISER TOUTES LES SESSIONS (MAINTENANCE)
-- =====================================================

-- Déconnecter tous les utilisateurs (utile pour maintenance)
UPDATE users SET session_active = 0, date_derniere_deconnexion = NOW();
