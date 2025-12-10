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

def check_problematic_users():
    """
    Vérifie tous les utilisateurs qui ont session_active=1 mais derniere_connexion=NULL
    Ces utilisateurs apparaîtront comme déconnectés dans l'admin malgré être actifs
    """
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Trouver les utilisateurs avec session_active=1 mais derniere_connexion=NULL
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            WHERE session_active = 1 AND derniere_connexion IS NULL
            ORDER BY id
        """)
        users = cursor.fetchall()
        
        if users:
            print("⚠️  UTILISATEURS AVEC PROBLÈMES (session_active=1 mais derniere_connexion=NULL) :")
            print("=" * 80)
            for user in users:
                print(f"ID: {user['id']:2d} | {user['prenom']} {user['nom']:<20} | {user['email']}")
        else:
            print("✅ Aucun utilisateur avec le problème session_active=1 mais derniere_connexion=NULL")
            
        # Vérifier également les utilisateurs avec derniere_connexion mais session_active=0
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            WHERE session_active = 0 AND derniere_connexion IS NOT NULL
            ORDER BY derniere_connexion DESC
            LIMIT 5
        """)
        users2 = cursor.fetchall()
        
        if users2:
            print("\nℹ️  UTILISATEURS DÉCONNECTÉS AVEC ANCIENNE CONNEXION :")
            print("=" * 80)
            for user in users2:
                print(f"ID: {user['id']:2d} | {user['prenom']} {user['nom']:<20} | {user['email']:<25} | Dernière connexion: {user['derniere_connexion']}")
                
    except Exception as e:
        print(f"Query Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("Vérification des utilisateurs avec problèmes de statut de connexion")
    print("=" * 80)
    check_problematic_users()