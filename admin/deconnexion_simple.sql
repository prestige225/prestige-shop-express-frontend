-- Ajout déconnexion à la table users
USE gestion_utilisateurs;

ALTER TABLE users
ADD COLUMN session_active BOOLEAN DEFAULT FALSE,
ADD COLUMN token_session VARCHAR(255) NULL,
ADD COLUMN date_derniere_deconnexion TIMESTAMP NULL,
ADD COLUMN ip_derniere_deconnexion VARCHAR(45) NULL;

CREATE INDEX idx_session_active ON users(session_active);
CREATE INDEX idx_token_session ON users(token_session);

-- Requêtes simples :
-- Connexion : UPDATE users SET session_active = TRUE, token_session = 'abc123', derniere_connexion = NOW(), ip_connexion = '192.168.1.1' WHERE id = 1;
-- Déconnexion : UPDATE users SET session_active = FALSE, date_derniere_deconnexion = NOW(), ip_derniere_deconnexion = '192.168.1.1' WHERE token_session = 'abc123';
-- Voir connectés : SELECT * FROM users WHERE session_active = TRUE;
