"""
Script pour vérifier la configuration email locale
"""
import os

def verifier_configuration():
    """Vérifier la configuration email"""
    print("🔍 Vérification de la configuration email...")
    print("=" * 50)
    
    # Vérifier les variables d'environnement
    gmail_address = os.environ.get('GMAIL_ADDRESS')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    print(f"📧 GMAIL_ADDRESS: {gmail_address if gmail_address else '❌ NON CONFIGURÉE'}")
    print(f"🔑 GMAIL_APP_PASSWORD: {'✅ CONFIGURÉE' if gmail_password else '❌ NON CONFIGURÉE'}")
    
    if gmail_password:
        print(f"📏 Longueur du mot de passe: {len(gmail_password)} caractères")
        # Afficher les 4 premiers et 4 derniers caractères seulement
        if len(gmail_password) >= 8:
            print(f"👁️  Aperçu: {gmail_password[:4]}****{gmail_password[-4:]}")
    
    print("\n📋 Instructions:")
    if not gmail_address:
        print("   ❌ Configurez GMAIL_ADDRESS")
    if not gmail_password:
        print("   ❌ Configurez GMAIL_APP_PASSWORD")
    
    if gmail_address and gmail_password:
        print("   ✅ Configuration complète")
        print("   🧪 Testez maintenant l'envoi d'email")
    
    return gmail_address and gmail_password

if __name__ == "__main__":
    verifier_configuration()