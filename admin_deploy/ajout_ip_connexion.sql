-- Ajout de la colonne ip_connexion manquante
USE gestion_utilisateurs;

ALTER TABLE users ADD COLUMN ip_connexion VARCHAR(45) NULL;

-- Maintenant vous pouvez utiliser les requêtes de connexion
UPDATE users SET session_active = 1, token_session = 'marie_token_789', derniere_connexion = NOW(), ip_connexion = '192.168.1.102' WHERE id = 3;

-- Autres exemples qui fonctionnent maintenant :
UPDATE users SET session_active = 1, token_session = 'admin_token_123', derniere_connexion = NOW(), ip_connexion = '192.168.1.100' WHERE id = 1;
UPDATE users SET session_active = 1, token_session = 'jean_token_456', derniere_connexion = NOW(), ip_connexion = '192.168.1.101' WHERE id = 2;
