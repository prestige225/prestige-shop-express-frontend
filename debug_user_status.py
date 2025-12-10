import mysql.connector
import os
from datetime import datetime, timedelta

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

def debug_user(email):
    """
    Debug l'état exact d'un utilisateur
    """
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    try:
        print(f"🔍 DEBUG DE L'UTILISATEUR : {email}")
        print("=" * 50)
        
        # Récupérer l'utilisateur
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            WHERE email = %s
        """, (email,))
        user = cursor.fetchone()
        
        if not user:
            print(f"❌ Aucun utilisateur trouvé avec l'email : {email}")
            return
            
        print(f"ID: {user['id']}")
        print(f"Nom: {user['prenom']} {user['nom']}")
        print(f"Email: {user['email']}")
        print(f"Statut: {user['statut']}")
        print(f"Session active: {user['session_active']}")
        print(f"Dernière connexion: {user['derniere_connexion']}")
        
        # Calculer si l'utilisateur est techniquement connecté
        is_connected = False
        if user['session_active'] == 1 and user['derniere_connexion']:
            # Vérifier si la dernière connexion est dans les 30 dernières minutes
            if isinstance(user['derniere_connexion'], str):
                last_conn = datetime.strptime(user['derniere_connexion'], '%Y-%m-%d %H:%M:%S')
            else:
                last_conn = user['derniere_connexion']
                
            if last_conn >= datetime.now() - timedelta(minutes=30):
                is_connected = True
        
        print(f"\n📊 ANALYSE :")
        print(f"L'utilisateur est techniquement {'CONNECTÉ' if is_connected else 'DÉCONNECTÉ'}")
        
        if is_connected:
            print("✅ Tout fonctionne correctement!")
        else:
            if user['session_active'] == 0:
                print("⚠️  session_active = 0 (l'utilisateur n'est pas connecté)")
            if not user['derniere_connexion']:
                print("⚠️  derniere_connexion = NULL (pas de date de connexion)")
            if user['derniere_connexion'] and not is_connected:
                print("⚠️  dernière connexion trop ancienne (plus de 30 minutes)")
                
    except Exception as e:
        print(f"❌ Erreur : {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Remplacez par l'email de l'utilisateur concerné
    email = input("Entrez l'email de l'utilisateur à debugger : ")
    debug_user(email)