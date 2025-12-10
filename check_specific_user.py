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

def check_user(email):
    conn = get_db_connection()
    if not conn:
        return
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Vérifier si l'utilisateur existe
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            WHERE email = %s
        """, (email,))
        user = cursor.fetchone()
        
        if user:
            print(f"Utilisateur trouvé :")
            print(f"ID: {user['id']}")
            print(f"Nom: {user['prenom']} {user['nom']}")
            print(f"Email: {user['email']}")
            print(f"Statut: {user['statut']}")
            print(f"Session active: {user['session_active']}")
            print(f"Dernière connexion: {user['derniere_connexion']}")
            
            # Si derniere_connexion est NULL, mettons-le à jour
            if user['derniere_connexion'] is None and user['session_active'] == 1:
                print("\n⚠️  L'utilisateur a session_active=1 mais derniere_connexion=NULL")
                print("Mise à jour en cours...")
                
                cursor.execute("""
                    UPDATE users 
                    SET derniere_connexion = NOW()
                    WHERE id = %s
                """, (user['id'],))
                conn.commit()
                
                print("✅ Mise à jour effectuée avec succès!")
                
                # Vérifier la mise à jour
                cursor.execute("""
                    SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
                    FROM users
                    WHERE id = %s
                """, (user['id'],))
                updated_user = cursor.fetchone()
                print(f"\nAprès mise à jour :")
                print(f"Dernière connexion: {updated_user['derniere_connexion']}")
            elif user['derniere_connexion'] is None:
                print("\nℹ️  L'utilisateur a derniere_connexion=NULL mais session_active=0")
                print("Cela signifie qu'il n'est pas connecté.")
            else:
                print("\n✅ L'utilisateur a déjà une date de dernière connexion valide.")
        else:
            print(f"Aucun utilisateur trouvé avec l'email : {email}")
            
    except Exception as e:
        print(f"Query Error: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Vérifier l'utilisateur mentionné
    email = "emileafanou182@gmail.com"
    print(f"Vérification de l'utilisateur avec l'email : {email}")
    print("-" * 50)
    check_user(email)