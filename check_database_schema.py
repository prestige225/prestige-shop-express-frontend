import mysql.connector
import os

# Configuration de la base de données
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com'),
    'user': os.environ.get('DB_USER', 'usblj9n0kraq8uoc'),
    'password': os.environ.get('DB_PASSWORD', '4fcY691gsJlwoQnk5xwa'),
    'database': os.environ.get('DB_NAME', 'bracv1wswmu4vsqxycku'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def get_db_connection():
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"DB Error: {e}")
        return None

def check_users_table_schema():
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor()
    try:
        # Obtenir la structure de la table users
        cursor.execute("DESCRIBE users")
        columns = cursor.fetchall()
        
        print("Structure de la table 'users':")
        print("Nom de la colonne\tType\t\tNull\tKey\tDefault\tExtra")
        print("-" * 60)
        for column in columns:
            print(f"{column[0]}\t\t\t{column[1]}\t{column[2]}\t{column[3]}\t{column[4]}\t{column[5]}")
            
        # Vérifier si les colonnes nécessaires existent
        required_columns = ['session_active', 'derniere_connexion', 'token_session']
        existing_columns = [col[0] for col in columns]
        
        print("\nVérification des colonnes requises:")
        for col in required_columns:
            status = "✓ Présente" if col in existing_columns else "✗ Absente"
            print(f"- {col}: {status}")
            
    except Exception as e:
        print(f"Query Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_users_table_schema()