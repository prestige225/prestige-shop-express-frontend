import mysql.connector
from mysql.connector import Error

# Configuration de la base de données (identique à celle du serveur)
DB_CONFIG = {
    'host': 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com',
    'user': 'usblj9n0kraq8uoc',
    'password': '4fcY691gsJlwoQnk5xwa',
    'database': 'bracv1wswmu4vsqxycku',
    'port': 3306
}

def get_db_connection():
    """Créer une connexion à la base de données"""
    try:
        print("Tentative de connexion à MySQL...")
        conn = mysql.connector.connect(**DB_CONFIG)
        print("✅ Connexion MySQL réussie")
        return conn
    except Error as e:
        print(f"❌ Erreur de connexion à MySQL: {e}")
        return None
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return None

def create_products_table():
    """Créer la table produits"""
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor()
    
    try:
        # Utiliser la base de données
        cursor.execute("USE bracv1wswmu4vsqxycku")
        
        # Supprimer la table si elle existe déjà
        cursor.execute("DROP TABLE IF EXISTS produits")
        
        # Créer la table produits
        create_table_query = """
        CREATE TABLE produits (
            id INT AUTO_INCREMENT PRIMARY KEY,
            nom VARCHAR(255) NOT NULL,
            description TEXT,
            prix DECIMAL(10, 2) NOT NULL,
            categorie VARCHAR(100),
            image_url VARCHAR(500),
            images_urls JSON,
            taille_disponible JSON,
            couleur_disponible JSON,
            stock INT DEFAULT 0,
            statut ENUM('actif', 'inactif', 'epuise') DEFAULT 'actif',
            date_creation TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            date_mise_a_jour TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
        )
        """
        cursor.execute(create_table_query)
        
        # Créer les index
        cursor.execute("CREATE INDEX idx_categorie ON produits(categorie)")
        cursor.execute("CREATE INDEX idx_statut ON produits(statut)")
        cursor.execute("CREATE INDEX idx_prix ON produits(prix)")
        
        # Insérer quelques produits de test
        insert_products_query = """
        INSERT INTO produits (nom, description, prix, categorie, image_url, images_urls, taille_disponible, couleur_disponible, stock) VALUES
        (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        products_data = [
            ('Chaussures de sport', 'Chaussures de sport confortables pour hommes, idéales pour la course à pied et le fitness.', 89.99, 'Chaussures', 'images/chaussures_sport.jpg', 
            '["images/chaussures_sport_1.jpg", "images/chaussures_sport_2.jpg", "images/chaussures_sport_3.jpg"]', 
            '["39", "40", "41", "42", "43", "44"]', 
            '["Noir", "Blanc", "Bleu"]', 50),
            
            ('T-shirt en coton', 'T-shirt 100% coton, respirant et confortable pour un usage quotidien.', 24.99, 'Vêtements', 'images/tshirt.jpg',
            '["images/tshirt_1.jpg", "images/tshirt_2.jpg"]',
            '["S", "M", "L", "XL", "XXL"]',
            '["Rouge", "Bleu", "Vert", "Noir"]', 100),
            
            ('Sac à dos étudiant', 'Sac à dos spacieux avec plusieurs compartiments, idéal pour l\'école ou le travail.', 59.99, 'Accessoires', 'images/sac_a_dos.jpg',
            '["images/sac_a_dos_1.jpg", "images/sac_a_dos_2.jpg", "images/sac_a_dos_3.jpg"]',
            '[]',
            '["Noir", "Gris", "Bleu"]', 30),
            
            ('Montre connectée', 'Montre intelligente avec suivi d\'activité, notifications et autonomie de 7 jours.', 129.99, 'Électronique', 'images/montre_connectee.jpg',
            '["images/montre_connectee_1.jpg", "images/montre_connectee_2.jpg"]',
            '[]',
            '["Noir", "Argent", "Or"]', 25),
            
            ('Casque audio sans fil', 'Casque Bluetooth avec réduction de bruit active et qualité sonore exceptionnelle.', 149.99, 'Électronique', 'images/casque_audio.jpg',
            '["images/casque_audio_1.jpg", "images/casque_audio_2.jpg", "images/casque_audio_3.jpg"]',
            '[]',
            '["Noir", "Blanc", "Rouge"]', 40)
        ]
        
        cursor.executemany(insert_products_query, products_data)
        
        conn.commit()
        print("✅ Table produits créée avec succès et données insérées")
        return True
        
    except Error as e:
        print(f"❌ Erreur lors de la création de la table: {e}")
        conn.rollback()
        return False
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 Création de la table produits...")
    if create_products_table():
        print("✅ Processus terminé avec succès")
    else:
        print("❌ Échec du processus")