#!/usr/bin/env python3
"""
Script pour initialiser la table des visites dans la base de données
"""
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la base de données
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com'),
    'user': os.environ.get('DB_USER', 'usblj9n0kraq8uoc'),
    'password': os.environ.get('DB_PASSWORD', '4fcY691gsJlwoQnk5xwa'),
    'database': os.environ.get('DB_NAME', 'bracv1wswmu4vsqxycku'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def create_visits_table():
    """Créer la table des visites si elle n'existe pas"""
    try:
        print("Tentative de connexion à MySQL...")
        conn = mysql.connector.connect(**DB_CONFIG)
        
        if conn.is_connected():
            print("✅ Connexion MySQL réussie")
            cursor = conn.cursor()
            
            # Créer la table des visites
            create_table_query = """
            CREATE TABLE IF NOT EXISTS visits (
              id INT AUTO_INCREMENT PRIMARY KEY,
              session_id VARCHAR(255) NOT NULL,
              ip_address VARCHAR(45) NULL,
              user_agent TEXT NULL,
              page_visited VARCHAR(500) NULL,
              referrer VARCHAR(500) NULL,
              language VARCHAR(10) NULL,
              screen_width INT NULL,
              screen_height INT NULL,
              url VARCHAR(1000) NULL,
              timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
              INDEX idx_session_id (session_id),
              INDEX idx_timestamp (timestamp),
              INDEX idx_ip_address (ip_address)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
            """
            
            cursor.execute(create_table_query)
            conn.commit()
            
            print("✅ Table 'visits' créée ou vérifiée avec succès")
            
            # Vérifier la structure de la table
            cursor.execute("DESCRIBE visits")
            columns = cursor.fetchall()
            print("\nStructure de la table 'visits':")
            for col in columns:
                print(f"  - {col[0]}: {col[1]} ({col[2]})")
            
            cursor.close()
            conn.close()
            print("\n✅ Connexion à MySQL fermée")
            
    except Error as e:
        print(f"❌ Erreur de connexion à MySQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("🚀 Initialisation de la table des visites...")
    success = create_visits_table()
    
    if success:
        print("\n🎉 La table des visites a été initialisée avec succès !")
        print("📊 Vous pouvez maintenant suivre les visites des utilisateurs non connectés.")
    else:
        print("\n❌ Échec de l'initialisation de la table des visites.")
        exit(1)