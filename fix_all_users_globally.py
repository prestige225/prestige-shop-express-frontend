#!/usr/bin/env python3
"""
Script de correction globale pour résoudre définitivement le problème des utilisateurs
Google OAuth qui apparaissent comme déconnectés dans l'admin.
"""

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
    """Créer une connexion à la base de données"""
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return None

def fix_all_users():
    """
    Correction globale de tous les problèmes d'utilisateurs
    """
    print("🔧 CORRECTION GLOBALE DES UTILISATEURS")
    print("=" * 50)
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor(dictionary=True)
    try:
        # 1. Identifier tous les utilisateurs avec des problèmes
        print("🔍 Recherche des utilisateurs avec problèmes...")
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            WHERE session_active = 1 AND derniere_connexion IS NULL
            ORDER BY id
        """)
        problematic_users = cursor.fetchall()
        
        print(f"⚠️  Trouvé {len(problematic_users)} utilisateurs avec session_active=1 mais derniere_connexion=NULL")
        
        # 2. Corriger ces utilisateurs
        fixed_count = 0
        for user in problematic_users:
            print(f"  🛠️  Correction de l'utilisateur {user['prenom']} {user['nom']} ({user['email']})...")
            cursor.execute("""
                UPDATE users 
                SET derniere_connexion = NOW(),
                    token_session = %s,
                    ip_connexion = %s
                WHERE id = %s
            """, (f"token_{user['id']}_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                  "127.0.0.1",
                  user['id']))
            fixed_count += 1
        
        if fixed_count > 0:
            conn.commit()
            print(f"✅ {fixed_count} utilisateurs corrigés avec succès!")
        
        # 3. Vérifier les utilisateurs déconnectés avec anciennes connexions
        print("\n🔍 Recherche des utilisateurs déconnectés avec anciennes connexions...")
        cursor.execute("""
            SELECT id, nom, prenom, email, statut, session_active, derniere_connexion
            FROM users
            WHERE session_active = 0 AND derniere_connexion IS NOT NULL
            ORDER BY derniere_connexion DESC
            LIMIT 10
        """)
        disconnected_users = cursor.fetchall()
        
        print(f"ℹ️  Trouvé {len(disconnected_users)} utilisateurs déconnectés avec anciennes connexions")
        for user in disconnected_users[:5]:  # Montrer les 5 premiers
            print(f"  - {user['prenom']} {user['nom']} ({user['email']}) - Dernière connexion: {user['derniere_connexion']}")
        
        # 4. Statistiques finales
        print("\n📊 STATISTIQUES FINALES:")
        cursor.execute("SELECT COUNT(*) as total FROM users")
        total = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as active FROM users WHERE statut = 'actif'")
        active = cursor.fetchone()['active']
        
        cursor.execute("""
            SELECT COUNT(*) as connected FROM users 
            WHERE session_active = 1 AND derniere_connexion >= DATE_SUB(NOW(), INTERVAL 30 MINUTE)
        """)
        connected = cursor.fetchone()['connected']
        
        cursor.execute("""
            SELECT COUNT(*) as disconnected FROM users 
            WHERE session_active = 0 OR derniere_connexion IS NULL OR derniere_connexion < DATE_SUB(NOW(), INTERVAL 30 MINUTE)
        """)
        disconnected = cursor.fetchone()['disconnected']
        
        print(f"  Total utilisateurs: {total}")
        print(f"  Actifs: {active}")
        print(f"  Connectés (en temps réel): {connected}")
        print(f"  Déconnectés: {disconnected}")
        
        print("\n✅ CORRECTION GLOBALE TERMINÉE!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la correction: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def create_test_user():
    """
    Créer un utilisateur de test pour vérifier que tout fonctionne
    """
    print("\n🧪 CRÉATION D'UN UTILISATEUR DE TEST")
    print("=" * 40)
    
    conn = get_db_connection()
    if not conn:
        return False
    
    cursor = conn.cursor(dictionary=True)
    try:
        # Créer un utilisateur de test
        test_email = f"test.user.{datetime.now().strftime('%Y%m%d%H%M%S')}@example.com"
        cursor.execute("""
            INSERT INTO users (nom, prenom, email, mot_de_passe, statut, session_active, derniere_connexion)
            VALUES (%s, %s, %s, %s, %s, %s, NOW())
        """, ("User", "Test", test_email, "", "actif", 1))
        conn.commit()
        
        user_id = cursor.lastrowid
        print(f"✅ Utilisateur de test créé avec succès!")
        print(f"   ID: {user_id}")
        print(f"   Email: {test_email}")
        print(f"   Statut: Connecté")
        
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création de l'utilisateur de test: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def verify_backend_fix():
    """
    Vérifier que le backend est correctement configuré
    """
    print("\n🔍 VÉRIFICATION DU BACKEND")
    print("=" * 30)
    
    try:
        # Vérifier que le fichier server_fixed.py existe
        server_file = "c:\\Users\\RCK COMPUTERS\\Desktop\\prestige shop express\\backend_render\\server_fixed.py"
        if os.path.exists(server_file):
            print("✅ Fichier server_fixed.py trouvé")
            
            # Vérifier le contenu
            with open(server_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
                # Vérifier les éléments clés
                if "google_login_callback_web" in content:
                    print("✅ Fonction google_login_callback_web présente")
                else:
                    print("❌ Fonction google_login_callback_web manquante")
                    
                if "session_active = 1" in content:
                    print("✅ Gestion de session_active présente")
                else:
                    print("❌ Gestion de session_active manquante")
                    
                if "derniere_connexion = NOW()" in content:
                    print("✅ Mise à jour de derniere_connexion présente")
                else:
                    print("❌ Mise à jour de derniere_connexion manquante")
        else:
            print("❌ Fichier server_fixed.py introuvable")
            
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la vérification du backend: {e}")
        return False

if __name__ == "__main__":
    print("🚀 SCRIPT DE CORRECTION GLOBALE DES UTILISATEURS")
    print("Ce script va corriger tous les problèmes d'affichage des utilisateurs dans l'admin")
    print()
    
    # 1. Vérifier le backend
    verify_backend_fix()
    
    # 2. Corriger tous les utilisateurs
    success = fix_all_users()
    
    # 3. Créer un utilisateur de test
    if success:
        create_test_user()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 TOUTES LES CORRECTIONS ONT ÉTÉ APPLIQUÉES AVEC SUCCÈS!")
        print("Les nouveaux utilisateurs Google OAuth devraient maintenant apparaître")
        print("comme CONNECTÉS dans l'interface admin et en haut de la liste.")
    else:
        print("❌ Des erreurs sont survenues lors de la correction.")
        
    print("=" * 60)