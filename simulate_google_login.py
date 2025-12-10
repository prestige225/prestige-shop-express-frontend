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
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"DB Error: {e}")
        return None

def simulate_google_login_success(user_id):
    """
    Simule une connexion réussie Google OAuth pour un utilisateur existant
    Cela met à jour les champs nécessaires pour que l'utilisateur apparaisse comme connecté
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Vérifier l'état actuel de l'utilisateur
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            WHERE id = %s
        """, (user_id,))
        user = cursor.fetchone()
        
        if not user:
            print(f"Aucun utilisateur trouvé avec l'ID : {user_id}")
            return False
            
        print(f"Avant la mise à jour :")
        print(f"ID: {user['id']}, Nom: {user['prenom']} {user['nom']}")
        print(f"Session active: {user['session_active']}")
        print(f"Dernière connexion: {user['derniere_connexion']}")
        
        # Mettre à jour l'utilisateur comme s'il venait de se connecter avec Google OAuth
        cursor.execute("""
            UPDATE users 
            SET session_active = 1,
                derniere_connexion = NOW(),
                token_session = %s,
                ip_connexion = %s,
                date_derniere_deconnexion = NULL,
                ip_derniere_deconnexion = NULL
            WHERE id = %s
        """, (f"token_{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}", 
              "127.0.0.1",  # IP simulée
              user_id))
        conn.commit()
        
        # Vérifier la mise à jour
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            WHERE id = %s
        """, (user_id,))
        updated_user = cursor.fetchone()
        
        print(f"\nAprès la mise à jour :")
        print(f"Session active: {updated_user['session_active']}")
        print(f"Dernière connexion: {updated_user['derniere_connexion']}")
        
        print(f"\n✅ L'utilisateur {updated_user['prenom']} {updated_user['nom']} est maintenant marqué comme connecté!")
        return True
        
    except Exception as e:
        print(f"Erreur lors de la mise à jour : {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Simuler la connexion pour l'utilisateur Emile Afanou (ID 47)
    user_id = 47
    print(f"Simulation de connexion Google OAuth pour l'utilisateur ID : {user_id}")
    print("-" * 60)
    simulate_google_login_success(user_id)