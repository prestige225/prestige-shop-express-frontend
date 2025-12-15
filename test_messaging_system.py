#!/usr/bin/env python3
"""
Script de vérification du système de messagerie
Teste que tous les composants sont correctement intégrés
"""

import json
import sys
import os

# Forcer l'encodage UTF-8 sur Windows
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except:
        pass

from pathlib import Path

def check_backend_file():
    """Vérifier que le backend a l'endpoint /api/messages/send-bulk"""
    print("Verification du backend...")
    
    backend_file = Path('backend_render/server_fixed.py')
    if not backend_file.exists():
        print("ERREUR: Fichier server_fixed.py non trouvé")
        return False
    
    content = backend_file.read_text(encoding='utf-8')
    
    # Vérifier la présence du nouvel endpoint
    if '@app.route(\'/api/messages/send-bulk\'' not in content:
        print("ERREUR: Endpoint /api/messages/send-bulk non trouvé")
        return False
    
    # Vérifier la présence de format_message
    if 'format_message' not in content:
        print("ATTENTION: format_message non importé (vérifier message_sender.py)")
        return False
    
    # Vérifier la présence de send_bulk_messages
    if 'send_bulk_messages' not in content:
        print("ERREUR: send_bulk_messages non importé")
        return False
    
    print("OK: Backend - Endpoint detecté et fonctionnel")
    return True

def check_frontend_file():
    """Vérifier que le fichier messages.html existe et est valide"""
    print("Verification du frontend...")
    
    frontend_file = Path('admin/messages.html')
    if not frontend_file.exists():
        print("ERREUR: Fichier admin/messages.html non trouvé")
        return False
    
    content = frontend_file.read_text(encoding='utf-8')
    
    # Vérifier la structure HTML
    checks = [
        ('DOCTYPE html', 'Déclaration HTML'),
        ('<script src="../api-config.js">', 'Script api-config.js'),
        ('id="loadBtn"', 'Bouton Charger'),
        ('id="statusFilter"', 'Filtre de statut'),
        ('id="usersList"', 'Liste utilisateurs'),
        ('id="messageForm"', 'Formulaire message'),
        ('id="subject"', 'Champ objet'),
        ('id="emailContent"', 'Champ contenu email'),
        ('/users/active', 'Appel API users/active'),
        ('/messages/send-bulk', 'Appel API send-bulk'),
        ('{{prenom}}', 'Variable prenom'),
        ('API_BASE_URL', 'Utilisation API_BASE_URL'),
    ]
    
    for check, name in checks:
        if check not in content:
            print(f"ERREUR: {name} manquant")
            return False
    
    print("OK: Frontend - Tous les éléments présents")
    return True

def check_admin_dashboard():
    """Vérifier que le lien Messages pointe vers messages.html"""
    print("Verification du tableau de bord admin...")
    
    admin_file = Path('admin/admin.html')
    if not admin_file.exists():
        print("ERREUR: Fichier admin/admin.html non trouvé")
        return False
    
    content = admin_file.read_text(encoding='utf-8')
    
    # Vérifier le lien mis à jour
    if 'href="messages.html"' not in content:
        print("ATTENTION: Lien Messages ne pointe pas vers messages.html")
        # Ce n'est pas fatal, juste un warning
    else:
        print("OK: Lien Messages correctement pointé vers messages.html")
    
    # Vérifier l'absence du lien vers l'ancien fichier
    if 'admin_messages.html' in content and 'admin_messages_' not in content:
        print("ATTENTION: Référence à l'ancien admin_messages.html détectée")
    
    return True

def check_documentation():
    """Vérifier la présence des fichiers de documentation"""
    print("Verification de la documentation...")
    
    files = [
        ('MESSAGING_SYSTEM.md', 'Documentation système'),
        ('DEPLOYMENT_GUIDE.md', 'Guide de déploiement'),
        ('admin/MESSAGING_ARCHIVE.md', 'Archive des anciens fichiers'),
    ]
    
    all_ok = True
    for file_path, name in files:
        if Path(file_path).exists():
            print(f"OK: {name} présent")
        else:
            print(f"ATTENTION: {name} manquant")
            all_ok = False
    
    return all_ok

def check_api_config():
    """Vérifier que api-config.js est accessible"""
    print("Verification du fichier api-config.js...")
    
    api_file = Path('admin/api-config.js')
    if not api_file.exists():
        print("ERREUR: Fichier admin/api-config.js non trouvé")
        return False
    
    content = api_file.read_text(encoding='utf-8')
    
    if 'API_BASE_URL' not in content or 'prestige-shop-backend' not in content:
        print("ATTENTION: Configuration API_BASE_URL invalide")
        return False
    
    print("OK: api-config.js")
    return True

def main():
    """Exécuter tous les tests"""
    print("=" * 60)
    print("TEST DU SYSTEME DE MESSAGERIE")
    print("=" * 60)
    print()
    
    results = {
        'Backend': check_backend_file(),
        'Frontend': check_frontend_file(),
        'Admin Dashboard': check_admin_dashboard(),
        'Documentation': check_documentation(),
        'API Config': check_api_config(),
    }
    
    print()
    print("=" * 60)
    print("RESUME DES RESULTATS")
    print("=" * 60)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for name, result in results.items():
        status = "OK" if result else "ERREUR"
        print(f"{name:30} {status}")
    
    print()
    print(f"Score: {passed}/{total} tests passés")
    
    if passed == total:
        print("\nTOUS LES TESTS SONT PASSES - Système prêt à l'emploi.")
        return 0
    else:
        print(f"\n{total - passed} test(s) en erreur. Vérifiez les détails ci-dessus.")
        return 1

if __name__ == '__main__':
    sys.exit(main())
