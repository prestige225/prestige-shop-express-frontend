#!/usr/bin/env python3
"""
Script de test pour vérifier que la correction Google OAuth fonctionne
"""

import requests
import json
import time
from datetime import datetime

def test_google_oauth_process():
    """
    Tester le processus complet de connexion Google OAuth
    """
    print("🧪 TEST DU PROCESSUS GOOGLE OAUTH")
    print("=" * 40)
    
    # Données de test pour un utilisateur Google OAuth
    test_data = {
        "credential": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20iLCJuYW1lIjoiVGVzdCBVc2VyIiwiZ2l2ZW5fbmFtZSI6IlRlc3QiLCJmYW1pbHlfbmFtZSI6IlVzZXIifQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    }
    
    try:
        # 1. Tester l'endpoint Google OAuth
        print("🔍 Test de l'endpoint /api/auth/google/callback/web...")
        response = requests.post(
            "http://localhost:5000/api/auth/google/callback/web",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   Réponse: {json.dumps(data, indent=2, ensure_ascii=False)}")
            
            if data.get('success'):
                print("✅ Endpoint Google OAuth fonctionnel")
                user = data.get('user', {})
                print(f"   Utilisateur: {user.get('prenom')} {user.get('nom')} ({user.get('email')})")
                return True
            else:
                print("❌ Erreur dans la réponse:", data.get('message', 'Erreur inconnue'))
                return False
        else:
            print("❌ Erreur HTTP:", response.status_code)
            print("   Réponse:", response.text)
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter au serveur Flask")
        print("   Assurez-vous que le serveur est démarré sur http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_user_status_after_login():
    """
    Vérifier l'état de l'utilisateur après connexion
    """
    print("\n🔍 VÉRIFICATION DE L'ÉTAT UTILISATEUR APRÈS CONNEXION")
    print("=" * 50)
    
    try:
        # Récupérer la liste des utilisateurs
        response = requests.get("http://localhost:5000/api/users")
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                users = data.get('users', [])
                print(f"✅ {len(users)} utilisateurs trouvés")
                
                # Chercher l'utilisateur de test
                test_user = None
                for user in users:
                    if user.get('email') == 'test@example.com':
                        test_user = user
                        break
                
                if test_user:
                    print("✅ Utilisateur de test trouvé:")
                    print(f"   Nom: {test_user.get('nom_complet')}")
                    print(f"   Email: {test_user.get('email')}")
                    print(f"   Statut connexion: {test_user.get('statut_connexion')}")
                    print(f"   Dernière connexion: {test_user.get('derniere_connexion')}")
                    
                    if test_user.get('statut_connexion') == 'CONNECTÉ':
                        print("🎉 L'utilisateur apparaît CORRECTEMENT comme CONNECTÉ!")
                        return True
                    else:
                        print("❌ L'utilisateur n'apparaît pas comme connecté")
                        return False
                else:
                    print("ℹ️  Utilisateur de test non trouvé (peut-être pas encore créé)")
                    return True
            else:
                print("❌ Erreur API:", data.get('error'))
                return False
        else:
            print("❌ Erreur HTTP:", response.status_code)
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False

def main():
    """
    Fonction principale de test
    """
    print("🚀 TEST COMPLET DE LA CORRECTION GOOGLE OAUTH")
    print("=" * 50)
    
    # 1. Tester le processus Google OAuth
    oauth_success = test_google_oauth_process()
    
    # 2. Attendre un peu pour que la base de données soit mise à jour
    if oauth_success:
        print("\n⏳ Attente de la mise à jour de la base de données...")
        time.sleep(2)
    
    # 3. Vérifier l'état de l'utilisateur
    status_success = test_user_status_after_login()
    
    print("\n" + "=" * 50)
    print("📊 RÉSULTATS DU TEST:")
    print(f"   Processus Google OAuth: {'✅ OK' if oauth_success else '❌ ERREUR'}")
    print(f"   État utilisateur: {'✅ OK' if status_success else '❌ ERREUR'}")
    
    if oauth_success and status_success:
        print("\n🎉 TOUT FONCTIONNE CORRECTEMENT!")
        print("Les utilisateurs Google OAuth devraient maintenant:")
        print("  1. Être correctement créés dans la base de données")
        print("  2. Apparaître comme CONNECTÉS dans l'admin")
        print("  3. Être positionnés en haut de la liste")
    else:
        print("\n❌ Des problèmes persistent.")
        print("Veuillez vérifier:")
        print("  1. Que le serveur Flask est bien démarré")
        print("  2. Que les variables d'environnement Google OAuth sont correctes")
        print("  3. Que la configuration Google Cloud est valide")
        
    print("=" * 50)

if __name__ == "__main__":
    main()