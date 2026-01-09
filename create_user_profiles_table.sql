-- MySQL schema for user_profiles
CREATE TABLE IF NOT EXISTS user_profiles (
  id INT AUTO_INCREMENT PRIMARY KEY,
  user_id INT NOT NULL,
  whatsapp VARCHAR(30) NOT NULL,
  adresse VARCHAR(255) NULL,
  sexe ENUM('Homme','Femme') NULL,
  statut ENUM('Élève','Étudiant','Parent','Professeur','Travailleur','Autre') NOT NULL,
  age INT NULL,
  centre_interet TEXT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT uq_user_profiles_user UNIQUE (user_id),
  CONSTRAINT fk_user_profiles_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
