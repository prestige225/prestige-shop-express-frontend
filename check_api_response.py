#!/usr/bin/env python3
import requests
import json

print("🔍 Vérification de la réponse API...")
response = requests.get("http://127.0.0.1:5000/api/produits?limit=5")

if response.status_code == 200:
    data = response.json()
    if data.get('produits'):
        print(f"\n✅ API retourne {len(data['produits'])} produits")
        print("\n📋 Vérification des champs recommande/moment:")
        
        for prod in data['produits'][:5]:
            print(f"\n   ID {prod.get('id')}: {prod.get('nom', 'N/A')[:40]}")
            print(f"      - recommande: {prod.get('recommande', 'N/A')} (type: {type(prod.get('recommande')).__name__})")
            print(f"      - moment: {prod.get('moment', 'N/A')} (type: {type(prod.get('moment')).__name__})")
else:
    print(f"❌ Erreur API: {response.status_code}")
