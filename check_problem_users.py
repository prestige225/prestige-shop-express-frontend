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

def check_problem_users():
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Chercher les utilisateurs avec session_active=1 mais derniere_connexion=NULL
        cursor.execute("""
            SELECT id, nom, prenom, email, session_active, derniere_connexion
            FROM users
            WHERE session_active = 1 AND derniere_connexion IS NULL
        """)
        users = cursor.fetchall()
        
        if users:
            print("PROBLEM USERS FOUND:")
            for user in users:
                print(f"ID: {user['id']}, Name: {user['prenom']} {user['nom']}, Email: {user['email']}")
        else:
            print("No problem users found.")
            
    except Exception as e:
        print(f"Query Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    check_problem_users()