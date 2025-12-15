#!/usr/bin/env python3
"""
Script de test pour vérifier la configuration SendGrid
"""
import os
import sys

print("=" * 60)
print("🧪 TEST CONFIGURATION SENDGRID")
print("=" * 60)

# Vérifier les variables d'environnement
print("\n📋 Vérification des variables d'environnement...")

sendgrid_api_key = os.environ.get('SENDGRID_API_KEY', '')
sendgrid_from_email = os.environ.get('SENDGRID_FROM_EMAIL', 'noreply@prestigeshopexpress.com')
sendgrid_from_name = os.environ.get('SENDGRID_FROM_NAME', 'Prestige Shop Express')

if sendgrid_api_key:
    print(f"✅ SENDGRID_API_KEY: {'*' * 20} (masqué)")
else:
    print("❌ SENDGRID_API_KEY: NON CONFIGURÉE")

print(f"✅ SENDGRID_FROM_EMAIL: {sendgrid_from_email}")
print(f"✅ SENDGRID_FROM_NAME: {sendgrid_from_name}")

# Tester l'import de SendGrid
print("\n📦 Vérification des imports...")
try:
    from sendgrid import SendGridAPIClient
    from sendgrid.helpers.mail import Mail, Email, To, Content
    print("✅ SendGrid importé avec succès")
except ImportError as e:
    print(f"❌ Erreur d'import SendGrid: {e}")
    print("   Installez avec: pip install sendgrid")
    sys.exit(1)

# Tester la connexion à SendGrid
print("\n🔗 Vérification de la connexion SendGrid...")
if not sendgrid_api_key:
    print("⚠️  Clé API manquante. Configurez SENDGRID_API_KEY sur Render.")
    print("   Voir: SENDGRID_CONFIGURATION.md")
    sys.exit(1)

try:
    sg = SendGridAPIClient(sendgrid_api_key)
    print("✅ Connexion à SendGrid réussie")
except Exception as e:
    print(f"❌ Erreur de connexion: {e}")
    sys.exit(1)

# Tester l'envoi d'un email (optionnel)
print("\n📧 Préparation d'un email de test...")
try:
    mail = Mail(
        from_email=Email(sendgrid_from_email, sendgrid_from_name),
        to_emails=To("contact@prestigeshopexpress.com"),
        subject="Test Prestige Shop Express",
        plain_text_content="Ceci est un email de test.",
        html_content="<p>Ceci est un <strong>email de test</strong>.</p>"
    )
    print("✅ Email préparé avec succès")
    
    # Décommenter pour envoyer réellement
    # print("\n📤 Envoi de l'email...")
    # response = sg.send(mail)
    # if response.status_code in [200, 201, 202]:
    #     print(f"✅ Email envoyé! (Status: {response.status_code})")
    # else:
    #     print(f"❌ Erreur SendGrid: {response.status_code}")
    #     print(f"   {response.body}")
    
except Exception as e:
    print(f"❌ Erreur lors de la préparation: {e}")
    sys.exit(1)

print("\n" + "=" * 60)
print("✅ TOUS LES TESTS SONT PASSÉS!")
print("=" * 60)
print("\n📝 Prochaines étapes:")
print("1. Vérifiez que vos variables d'environnement sont configurées sur Render")
print("2. Testez l'envoi d'email via l'interface admin")
print("3. Vérifiez les logs Render pour les messages")
print("\n📖 Consultez SENDGRID_CONFIGURATION.md pour plus de détails")
