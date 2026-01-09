-- Ajout déconnexion à votre table users existante
USE gestion_utilisateurs;

ALTER TABLE users
ADD COLUMN session_active BOOLEAN DEFAULT FALSE,
ADD COLUMN token_session VARCHAR(255) NULL,
ADD COLUMN date_derniere_deconnexion TIMESTAMP NULL,
ADD COLUMN ip_derniere_deconnexion VARCHAR(45) NULL;

CREATE INDEX idx_session_active ON users(session_active);
CREATE INDEX idx_token_session ON users(token_session);

-- Mettre à jour les utilisateurs de test avec des sessions actives pour tester
UPDATE users SET session_active = TRUE, token_session = 'token123' WHERE email = 'admin@test.com';
UPDATE users SET session_active = FALSE, token_session = 'token456', derniere_connexion = NOW() WHERE email = 'jean@test.com';
