#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de test local pour l'API Prestige Shop Express
Permet de vérifier que les routes API fonctionnent avant déploiement
"""

import requests
import json
import sys
from colorama import init, Fore, Style

# Initialiser colorama pour les couleurs dans la console
try:
    init()
except:
    pass

BASE_URL = "http://localhost:5000/api"

def print_separator():
    print("\n" + "="*80 + "\n")

def print_success(message):
    print(f"{Fore.GREEN}✅ {message}{Style.RESET_ALL}")

def print_error(message):
    print(f"{Fore.RED}❌ {message}{Style.RESET_ALL}")

def print_info(message):
    print(f"{Fore.BLUE}ℹ️  {message}{Style.RESET_ALL}")

def print_warning(message):
    print(f"{Fore.YELLOW}⚠️  {message}{Style.RESET_ALL}")

def test_endpoint(name, method, url, data=None, expected_status=200):
    """Tester un endpoint spécifique"""
    print_info(f"Test: {name}")
    print(f"  {Fore.CYAN}URL:{Style.RESET_ALL} {url}")
    print(f"  {Fore.CYAN}Méthode:{Style.RESET_ALL} {method}")
    
    try:
        if method == 'GET':
            response = requests.get(url, timeout=5)
        elif method == 'POST':
            response = requests.post(url, json=data, headers={'Content-Type': 'application/json'}, timeout=5)
        elif method == 'OPTIONS':
            response = requests.options(url, timeout=5)
        
        print(f"  {Fore.CYAN}Status:{Style.RESET_ALL} {response.status_code}")
        
        # Vérifier si c'est du JSON
        content_type = response.headers.get('Content-Type', '')
        print(f"  {Fore.CYAN}Content-Type:{Style.RESET_ALL} {content_type}")
        
        if 'application/json' in content_type:
            try:
                json_data = response.json()
                print(f"  {Fore.CYAN}Réponse:{Style.RESET_ALL}")
                print(json.dumps(json_data, indent=2, ensure_ascii=False))
                
                if response.status_code == expected_status:
                    print_success("✓ Test réussi\n")
                    return True
                else:
                    print_warning(f"✗ Status attendu: {expected_status}, reçu: {response.status_code}\n")
                    return False
                    
            except json.JSONDecodeError as e:
                print_error(f"✗ Erreur parsing JSON: {e}\n")
                print(f"  Contenu brut: {response.text[:200]}\n")
                return False
        else:
            print_error(f"✗ Le serveur a retourné du HTML au lieu de JSON!\n")
            print(f"  Contenu: {response.text[:300]}\n")
            return False
            
    except requests.exceptions.ConnectionError:
        print_error("✌️  Impossible de se connecter au serveur!")
        print(f"  Assurez-vous que le serveur tourne sur {BASE_URL}")
        print(f"  Lancez: python backend_render/server_fixed.py\n")
        return False
    except requests.exceptions.Timeout:
        print_error("✌️  Timeout - Le serveur a mis trop de temps à répondre\n")
        return False
    except Exception as e:
        print_error(f"✌️  Erreur: {str(e)}\n")
        return False

def main():
    """Exécuter tous les tests"""
    print_separator()
    print(f"{Fore.MAGENTA}🧪 Tests API - Prestige Shop Express{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Base URL:{Style.RESET_ALL} {BASE_URL}")
    print_separator()
    
    # Test 1: Endpoint de base
    success = test_endpoint(
        "Endpoint /test",
        "GET",
        f"{BASE_URL}/test",
        expected_status=200
    )
    
    # Test 2: Inscription (avec données de test)
    test_email = f"test_{int(__import__('time').time())}@example.com"
    success &= test_endpoint(
        "Inscription (/register)",
        "POST",
        f"{BASE_URL}/register",
        data={
            "nom": "Test User",
            "prenom": "Test",
            "email": test_email,
            "numero": "0102030405",
            "mot_de_passe": "testpassword123"
        },
        expected_status=201
    )
    
    # Test 3: Google OAuth Callback (avec fake token)
    success &= test_endpoint(
        "Google OAuth Callback (/auth/google/callback/web)",
        "POST",
        f"{BASE_URL}/auth/google/callback/web",
        data={
            "credential": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6InRlc3RAZXhhbXBsZS5jb20ifQ.fake"
        },
        expected_status=400  # Doit échouer car le token est faux, mais en JSON
    )
    
    # Test 4: Vérifier OPTIONS
    success &= test_endpoint(
        "OPTIONS /register",
        "OPTIONS",
        f"{BASE_URL}/register",
        expected_status=200
    )
    
    # Test 5: Route inexistante (doit retourner JSON 404)
    success &= test_endpoint(
        "Route inexistante (404)",
        "GET",
        f"{BASE_URL}/route-inexistante",
        expected_status=404
    )
    
    # Résumé
    print_separator()
    if success:
        print_success("🎉 Tous les tests sont passés avec succès!")
    else:
        print_error("💥 Certains tests ont échoué")
        print_warning("Vérifiez les logs ci-dessus pour plus de détails")
    
    print_separator()
    return 0 if success else 1

if __name__ == '__main__':
    sys.exit(main())
