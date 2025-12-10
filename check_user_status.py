import mysql.connector
import os
from datetime import datetime

# Configuration de la base de données
DB_CONFIG = {
    'host': os.environ.get('DB_HOST', 'bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com'),
    'user': os.environ.get('DB_USER', 'usblj9n0kraq8uoc'),
    'password': os.environ.get('DB_PASSWORD', '4fcY691gsJlwoQnk5xwa'),
    'database': os.environ.get('DB_NAME', 'bracv1wswmu4vsqxycku'),
    'port': int(os.environ.get('DB_PORT', 3306))
}

def get_db_connection():
    """Créer une connexion à la base de données"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Erreur de connexion: {e}")
        return None

def check_user_status():
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Récupérer les utilisateurs récents
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            ORDER BY derniere_connexion DESC
            LIMIT 10
        """)
        users = cursor.fetchall()
        
        print("ID\tNom\t\t\tEmail\t\t\t\tStatut\tSession\tDernière connexion")
        print("--\t---\t\t\t-----\t\t\t\t------\t-------\t------------------")
        
        for user in users:
            # Formater la date
            if user['derniere_connexion']:
                last_conn_str = user['derniere_connexion'].strftime('%Y-%m-%d %H:%M')
            else:
                last_conn_str = 'Jamais'
            
            session_status = 'Oui' if user['session_active'] == 1 else 'Non'
            
            print(f"{user['id']}\t{user['prenom']} {user['nom']}\t\t{user['email']}\t\t{user['statut']}\t{session_status}\t{last_conn_str}")
            
            # Vérifier les incohérences
            if not user['derniere_connexion'] and user['session_active'] == 1:
                print(f"\t⚠️  Problème: session_active=1 mais derniere_connexion=NULL")
        
        print(f"\nTotal: {len(users)} utilisateurs")
        
    except Exception as e:
        print(f"Erreur: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_user_status()