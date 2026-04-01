"""
Script de test pour vérifier que les produits recommandés et du moment sont bien renvoyés par l'API
"""

import requests
import json

# URL de l'API (ajustez selon votre environnement)
API_URL = "http://localhost:5000/api/produits"

print("🔍 Test de l'API des produits...")
print("=" * 60)

try:
    # Récupérer tous les produits
    response = requests.get(API_URL, params={"limit": 500, "offset": 0})
    
    if response.status_code == 200:
        data = response.json()
        
        if data.get('success'):
            produits = data.get('produits', [])
            print(f"✅ {len(produits)} produits récupérés")
            print("=" * 60)
            
            # Vérifier les produits recommandés
            recommandes = [p for p in produits if p.get('recommande') == 1]
            moments = [p for p in produits if p.get('moment') == 1]
            
            print(f"\n⭐ Produits recommandés: {len(recommandes)}")
            for p in recommandes[:5]:  # Afficher les 5 premiers
                print(f"  - {p['nom']} (ID: {p['id']}, Catégorie: {p['categorie']})")
            
            print(f"\n🔥 Produits du moment: {len(moments)}")
            for p in moments[:5]:  # Afficher les 5 premiers
                print(f"  - {p['nom']} (ID: {p['id']}, Catégorie: {p['categorie']})")
            
            print("\n" + "=" * 60)
            print("📊 Exemple de structure de produit:")
            if produits:
                exemple = produits[0]
                print(json.dumps({
                    "id": exemple.get('id'),
                    "nom": exemple.get('nom'),
                    "prix": exemple.get('prix'),
                    "categorie": exemple.get('categorie'),
                    "recommande": exemple.get('recommande'),
                    "moment": exemple.get('moment'),
                    "stock": exemple.get('stock')
                }, indent=2, ensure_ascii=False))
                
        else:
            print(f"❌ Erreur API: {data.get('message')}")
    else:
        print(f"❌ Erreur HTTP: {response.status_code}")
        
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")
    print("\n💡 Assurez-vous que le serveur backend est démarré sur http://localhost:5000")
