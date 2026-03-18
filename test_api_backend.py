#!/usr/bin/env python
# Script pour tester l'API du backend Render

import requests
import json

# Tester l'API du backend Render
urls_to_test = [
    'https://prestige-shop-backend.onrender.com/api/produits',
    'https://prestige-shop-backend.onrender.com/ping',
    'https://prestige-shop-backend.onrender.com/health',
]

print("🧪 Test des endpoints du backend Render...\n")

for url in urls_to_test:
    print(f"📍 Testant: {url}")
    try:
        response = requests.get(url, timeout=10)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                if 'produits' in data:
                    count = len(data.get('produits', []))
                    print(f"  ✅ Produits retournés: {count}")
                    if count > 0:
                        first = data['produits'][0]
                        print(f"  Premier produit: {first.get('nom', 'N/A')} ({first.get('id', 'N/A')})")
                else:
                    print(f"  Réponse JSON: {str(data)[:100]}...")
            except Exception as e:
                print(f"  Texte reçu: {response.text[:100]}...")
        else:
            print(f"  ❌ Erreur: {response.text[:100]}...")
    except requests.exceptions.Timeout:
        print(f"  ❌ Timeout après 10 secondes")
    except requests.exceptions.ConnectionError as e:
        print(f"  ❌ Impossible de se connecter: {e}")
    except Exception as e:
        print(f"  ❌ Erreur: {e}")
    
    print()
