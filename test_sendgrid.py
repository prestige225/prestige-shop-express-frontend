#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script de test pour SendGrid
Vérifie que les emails peuvent être envoyés correctement
"""

import os
import sys

def test_sendgrid():
    """Tester la configuration SendGrid"""
    
    print("=" * 60)
    print("🧪 TEST SENDGRID POUR PRESTIGE SHOP EXPRESS")
    print("=" * 60)
    print()
    
    # Vérifier les variables d'environnement
    print("1️⃣  Vérification des variables d'environnement...")
    print("-" * 60)
    
    sendgrid_api_key = os.environ.get('SENDGRID_API_KEY', '')
    sendgrid_from_email = os.environ.get('SENDGRID_FROM_EMAIL', '')
    sendgrid_from_name = os.environ.get('SENDGRID_FROM_NAME', '')
    
    if not sendgrid_api_key:
        print("❌ SENDGRID_API_KEY non défini")
        print("   💡 Ajoutez cette variable d'environnement sur Render")
        return False
    else:
        key_preview = sendgrid_api_key[:10] + '...' + sendgrid_api_key[-10:]
        print(f"✅ SENDGRID_API_KEY: {key_preview}")
    
    if not sendgrid_from_email:
        print("⚠️  SENDGRID_FROM_EMAIL non défini (valeur par défaut: noreply@prestigeshopexpress.com)")
    else:
        print(f"✅ SENDGRID_FROM_EMAIL: {sendgrid_from_email}")
    
    if not sendgrid_from_name:
        print("⚠️  SENDGRID_FROM_NAME non défini (valeur par défaut: Prestige Shop Express)")
    else:
        print(f"✅ SENDGRID_FROM_NAME: {sendgrid_from_name}")
    
    print()
    
    # Importer SendGrid
    print("2️⃣  Vérification de l'installation SendGrid...")
    print("-" * 60)
    
    try:
        from sendgrid import SendGridAPIClient
        from sendgrid.helpers.mail import Mail, Email, To
        print("✅ Modules SendGrid importés avec succès")
    except ImportError as e:
        print(f"❌ Erreur d'importation: {e}")
        print("   💡 Exécutez: pip install sendgrid")
        return False
    
    print()
    
    # Tester la connexion à SendGrid
    print("3️⃣  Test de connexion à l'API SendGrid...")
    print("-" * 60)
    
    try:
        sg = SendGridAPIClient(sendgrid_api_key)
        
        # Créer un email de test
        test_to_email = os.environ.get('TEST_EMAIL', 'test@example.com')
        
        # Demander l'email de destination
        if test_to_email == 'test@example.com':
            print("⚠️  Variable TEST_EMAIL non définie")
            test_to_email = input("📧 Entrez l'adresse email de destination pour le test: ").strip()
            if not test_to_email:
                print("❌ Pas d'adresse email fournie")
                return False
        
        print(f"📧 Envoi d'un email de test à: {test_to_email}")
        
        mail = Mail(
            from_email=Email(
                sendgrid_from_email or 'noreply@prestigeshopexpress.com',
                sendgrid_from_name or 'Prestige Shop Express'
            ),
            to_emails=To(test_to_email),
            subject='🧪 Test SendGrid - Prestige Shop Express',
            plain_text_content="""
Bonjour,

Ceci est un email de test pour vérifier que SendGrid fonctionne correctement.

Si vous recevez cet email, cela signifie que:
✅ L'API SendGrid est configurée correctement
✅ Les variables d'environnement sont définies
✅ L'adresse "From" est vérifiée

Vous pouvez maintenant envoyer des emails aux utilisateurs de Prestige Shop Express!

Cordialement,
L'équipe Prestige Shop Express
            """,
            html_content="""
<html>
    <body>
        <h2>🧪 Test SendGrid</h2>
        <p>Bonjour,</p>
        <p>Ceci est un email de test pour vérifier que SendGrid fonctionne correctement.</p>
        <p>Si vous recevez cet email, cela signifie que:</p>
        <ul>
            <li>✅ L'API SendGrid est configurée correctement</li>
            <li>✅ Les variables d'environnement sont définies</li>
            <li>✅ L'adresse "From" est vérifiée</li>
        </ul>
        <p>Vous pouvez maintenant envoyer des emails aux utilisateurs de Prestige Shop Express!</p>
        <p>Cordialement,<br>L'équipe Prestige Shop Express</p>
    </body>
</html>
            """
        )
        
        response = sg.send(mail)
        
        if response.status_code in [200, 201, 202]:
            print(f"✅ Email envoyé avec succès!")
            print(f"   Status Code: {response.status_code}")
            print(f"   Message ID: {response.headers.get('X-Message-Id', 'N/A')}")
            print()
            print("=" * 60)
            print("✅ TEST RÉUSSI!")
            print("=" * 60)
            print()
            print("📝 Prochaines étapes:")
            print("1. Vérifiez votre boîte mail (et spam)")
            print("2. Allez sur le dashboard Prestige Shop Express")
            print("3. Testez l'envoi de messages aux utilisateurs")
            print("4. Vérifiez les logs sur https://app.sendgrid.com/")
            return True
        else:
            print(f"❌ Erreur SendGrid: {response.status_code}")
            print(f"   Body: {response.body}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_sendgrid()
    sys.exit(0 if success else 1)
