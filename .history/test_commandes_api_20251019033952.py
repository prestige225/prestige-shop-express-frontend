# Test des routes API pour la gestion des commandes
# Prestige Shop Express

import requests
import json

BASE_URL = "http://localhost:5000"

def test_get_all_commandes():
    """Test de récupération de toutes les commandes"""
    print("\n🔍 Test: Récupération de toutes les commandes")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/commandes")
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Success: {data.get('success')}")
        print(f"Nombre de commandes: {len(data.get('data', []))}")
        
        if data.get('success') and data.get('data'):
            print("\nPremière commande:")
            print(json.dumps(data['data'][0], indent=2, default=str))
        
        return data.get('success', False)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_create_commande():
    """Test de création d'une commande"""
    print("\n📝 Test: Création d'une nouvelle commande")
    print("=" * 50)
    
    commande_data = {
        "user_id": 1,  # Remplacer par un user_id valide
        "montant_total": 35000.00,
        "adresse_livraison": "Test Adresse, Cocody, Abidjan",
        "telephone": "0758415088",
        "notes": "Commande de test"
    }
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/commandes",
            json=commande_data,
            headers={'Content-Type': 'application/json'}
        )
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
        
        if data.get('success'):
            print(f"Numéro de commande: {data.get('numero_commande')}")
            print(f"ID de commande: {data.get('commande_id')}")
            return data.get('commande_id')
        
        return None
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return None

def test_get_commande_detail(commande_id):
    """Test de récupération des détails d'une commande"""
    print(f"\n🔍 Test: Récupération des détails de la commande {commande_id}")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/commandes/{commande_id}")
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Success: {data.get('success')}")
        
        if data.get('success'):
            print("\nDétails de la commande:")
            print(json.dumps(data['data'], indent=2, default=str))
        
        return data.get('success', False)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_update_commande(commande_id):
    """Test de mise à jour d'une commande"""
    print(f"\n✏️ Test: Mise à jour de la commande {commande_id}")
    print("=" * 50)
    
    update_data = {
        "statut": "en_cours"
    }
    
    try:
        response = requests.put(
            f"{BASE_URL}/api/commandes/{commande_id}",
            json=update_data,
            headers={'Content-Type': 'application/json'}
        )
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Success: {data.get('success')}")
        print(f"Message: {data.get('message')}")
        
        return data.get('success', False)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_get_user_commandes(user_id):
    """Test de récupération des commandes d'un utilisateur"""
    print(f"\n👤 Test: Récupération des commandes de l'utilisateur {user_id}")
    print("=" * 50)
    
    try:
        response = requests.get(f"{BASE_URL}/api/commandes/user/{user_id}")
        data = response.json()
        
        print(f"Status Code: {response.status_code}")
        print(f"Success: {data.get('success')}")
        print(f"Nombre de commandes: {len(data.get('data', []))}")
        
        return data.get('success', False)
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Exécuter tous les tests"""
    print("\n" + "=" * 50)
    print("🧪 TESTS DES ROUTES API - GESTION DES COMMANDES")
    print("=" * 50)
    
    # Test 1: Récupérer toutes les commandes
    test_get_all_commandes()
    
    # Test 2: Créer une nouvelle commande
    new_commande_id = test_create_commande()
    
    if new_commande_id:
        # Test 3: Récupérer les détails de la commande créée
        test_get_commande_detail(new_commande_id)
        
        # Test 4: Mettre à jour la commande
        test_update_commande(new_commande_id)
        
        # Test 5: Vérifier la mise à jour
        test_get_commande_detail(new_commande_id)
    
    # Test 6: Récupérer les commandes d'un utilisateur
    test_get_user_commandes(1)  # Remplacer par un user_id valide
    
    print("\n" + "=" * 50)
    print("✅ Tests terminés!")
    print("=" * 50)

if __name__ == "__main__":
    main()
