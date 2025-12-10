import mysql.connector
import os
import datetime
import random

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

def simulate_complete_google_oauth_process(email, first_name, last_name):
    """
    Simule le processus complet de connexion Google OAuth
    """
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor(dictionary=True)
    try:
        print(f"🔍 Recherche de l'utilisateur avec l'email : {email}")
        
        # Vérifier si l'utilisateur existe déjà
        cursor.execute("SELECT id, nom, prenom, email, statut FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            print(f"👤 Utilisateur trouvé : {user['prenom']} {user['nom']} (ID: {user['id']})")
            
            # Mettre à jour l'utilisateur comme s'il venait de se connecter
            print("🔄 Mise à jour de l'utilisateur existant...")
            cursor.execute("""
                UPDATE users 
                SET prenom = %s, 
                    nom = %s, 
                    derniere_connexion = NOW(), 
                    session_active = 1, 
                    token_session = %s, 
                    ip_connexion = %s,
                    date_derniere_deconnexion = NULL,
                    ip_derniere_deconnexion = NULL
                WHERE id = %s
            """, (first_name, 
                  last_name, 
                  f"token_{user['id']}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
                  f"192.168.1.{random.randint(1, 255)}",
                  user['id']))
            conn.commit()
            
            user_id = user['id']
            print(f"✅ Utilisateur mis à jour avec succès!")
        else:
            print("🆕 Création d'un nouvel utilisateur...")
            # Créer un nouvel utilisateur
            cursor.execute("""
                INSERT INTO users (nom, prenom, email, mot_de_passe, statut, session_active)
                VALUES (%s, %s, %s, %s, 'actif', 1)
            """, (last_name, first_name, email, ''))
            conn.commit()
            
            # Récupérer l'ID du nouvel utilisateur
            user_id = cursor.lastrowid
            
            # Mettre à jour immédiatement les informations de connexion
            cursor.execute("""
                UPDATE users 
                SET derniere_connexion = NOW(), 
                    token_session = %s, 
                    ip_connexion = %s,
                    date_derniere_deconnexion = NULL,
                    ip_derniere_deconnexion = NULL
                WHERE id = %s
            """, (f"token_{user_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{random.randint(1000, 9999)}",
                  f"192.168.1.{random.randint(1, 255)}",
                  user_id))
            conn.commit()
            
            print(f"✅ Nouvel utilisateur créé avec ID: {user_id}")
        
        # Vérifier l'état final de l'utilisateur
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            WHERE id = %s
        """, (user_id,))
        final_user = cursor.fetchone()
        
        print(f"\n📋 ÉTAT FINAL DE L'UTILISATEUR :")
        print(f"ID: {final_user['id']}")
        print(f"Nom: {final_user['prenom']} {final_user['nom']}")
        print(f"Email: {final_user['email']}")
        print(f"Statut: {final_user['statut']}")
        print(f"Session active: {final_user['session_active']}")
        print(f"Dernière connexion: {final_user['derniere_connexion']}")
        
        # Vérifier si l'utilisateur apparaîtrait comme connecté dans l'admin
        if final_user['session_active'] == 1 and final_user['derniere_connexion']:
            print(f"\n✅ L'utilisateur apparaîtra comme CONNECTÉ dans l'interface admin!")
        else:
            print(f"\n⚠️  L'utilisateur apparaîtra comme DÉCONNECTÉ (session_active=0 ou derniere_connexion=NULL)")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la simulation : {e}")
        return False
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    print("🧪 SIMULATION COMPLÈTE DU PROCESSUS GOOGLE OAUTH")
    print("=" * 60)
    
    # Simuler un utilisateur qui se connecte avec Google
    email = "test.google.oauth@example.com"
    first_name = "Test"
    last_name = "GoogleUser"
    
    print(f"Email: {email}")
    print(f"Prénom: {first_name}")
    print(f"Nom: {last_name}")
    print("-" * 60)
    
    success = simulate_complete_google_oauth_process(email, first_name, last_name)
    
    if success:
        print(f"\n🎉 Simulation terminée avec succès!")
    else:
        print(f"\n❌ La simulation a échoué!")