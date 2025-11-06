-- Script de création de la table commandes
-- Prestige Shop Express

-- Création de la table commandes
CREATE TABLE IF NOT EXISTS commandes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    numero_commande VARCHAR(50) NOT NULL UNIQUE,
    date_commande DATETIME DEFAULT CURRENT_TIMESTAMP,
    statut ENUM('en_attente', 'en_cours', 'livree', 'annulee') DEFAULT 'en_attente',
    montant_total DECIMAL(10,2) NOT NULL,
    adresse_livraison TEXT NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    notes TEXT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_statut (statut),
    INDEX idx_date_commande (date_commande)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Ajout de quelques commandes de test (optionnel)
-- Remplacer les user_id par des IDs valides de votre table users

-- Exemple de commande 1
INSERT INTO commandes (user_id, numero_commande, montant_total, adresse_livraison, telephone, statut, notes) VALUES
(1, 'CMD-20241019120000-123', 45000.00, 'Cocody Angré 7ème Tranche, Abidjan, Côte d\'Ivoire', '0758415088', 'en_attente', 'Livraison avant 18h svp');

-- Exemple de commande 2
INSERT INTO commandes (user_id, numero_commande, montant_total, adresse_livraison, telephone, statut, notes) VALUES
(1, 'CMD-20241018153000-456', 28500.00, 'Yopougon Siporex, Abidjan', '0709876543', 'en_cours', '');

-- Exemple de commande 3
INSERT INTO commandes (user_id, numero_commande, montant_total, adresse_livraison, telephone, statut) VALUES
(2, 'CMD-20241017094500-789', 67800.00, 'Plateau, immeuble SCIAM, 3ème étage', '0756123456', 'livree');

-- Vérification de la création
SELECT COUNT(*) as total_commandes FROM commandes;
SELECT * FROM commandes ORDER BY date_commande DESC LIMIT 5;
