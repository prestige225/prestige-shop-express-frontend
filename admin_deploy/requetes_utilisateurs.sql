-- =====================================================
-- VOTRE TABLE USERS EST DÉJÀ MISE À JOUR !
-- UTILISEZ CES REQUÊTES POUR LA DÉCONNEXION
-- =====================================================

USE gestion_utilisateurs;

-- =====================================================
-- REQUÊTES POUR LA CONNEXION
-- =====================================================

-- 1. Connexion utilisateur (quand quelqu'un se connecte)
-- UPDATE users SET session_active = TRUE, token_session = 'abc123', derniere_connexion = NOW(), ip_connexion = '192.168.1.1' WHERE id = 1;

-- 2. Déconnexion utilisateur (quand quelqu'un se déconnecte)
-- UPDATE users SET session_active = FALSE, date_derniere_deconnexion = NOW(), ip_derniere_deconnexion = '192.168.1.1' WHERE token_session = 'abc123';

-- =====================================================
-- REQUÊTES POUR VOIR LES UTILISATEURS
-- =====================================================

-- 3. Voir tous les utilisateurs connectés actuellement
-- SELECT * FROM users WHERE session_active = TRUE;

-- 4. Voir tous les utilisateurs inscrits avec leur statut de connexion
-- SELECT id, CONCAT(prenom, ' ', nom) as nom_complet, email, statut, session_active, derniere_connexion FROM users ORDER BY derniere_connexion DESC;

-- 5. Compter le nombre d'utilisateurs connectés
-- SELECT COUNT(*) as connectes FROM users WHERE session_active = TRUE;

-- =====================================================
-- EXEMPLES CONCRETS AVEC VOS DONNÉES DE TEST
-- =====================================================

-- Connecter l'admin :
-- UPDATE users SET session_active = TRUE, token_session = 'admin_token_123', derniere_connexion = NOW(), ip_connexion = '192.168.1.100' WHERE email = 'admin@test.com';

-- Connecter Jean Dupont :
-- UPDATE users SET session_active = TRUE, token_session = 'jean_token_456', derniere_connexion = NOW(), ip_connexion = '192.168.1.101' WHERE email = 'jean@test.com';

-- Voir qui est connecté :
-- SELECT CONCAT(prenom, ' ', nom) as nom, email, derniere_connexion FROM users WHERE session_active = TRUE;

-- Déconnecter l'admin avec son token :
-- UPDATE users SET session_active = FALSE, date_derniere_deconnexion = NOW(), ip_derniere_deconnexion = '192.168.1.100' WHERE token_session = 'admin_token_123';

-- =====================================================
-- SUPPRESSION D'UTILISATEURS
-- =====================================================

-- 6. Suspendre un utilisateur (au lieu de supprimer définitivement)
-- UPDATE users SET statut = 'suspendu' WHERE id = 1;

-- 7. Supprimer définitivement un utilisateur
-- DELETE FROM users WHERE id = 1;

-- 8. Voir seulement les utilisateurs actifs
-- SELECT * FROM users WHERE statut = 'actif';

-- =====================================================
-- RÉSUMÉ DES FONCTIONNALITÉS
-- =====================================================

-- ✅ Utilisateurs inscrits : SELECT * FROM users WHERE statut = 'actif';
-- ✅ Utilisateurs connectés : SELECT * FROM users WHERE session_active = TRUE;
-- ✅ Déconnexion : UPDATE users SET session_active = FALSE WHERE token_session = 'xxx';
-- ✅ Suppression : UPDATE users SET statut = 'suspendu' WHERE id = x;
