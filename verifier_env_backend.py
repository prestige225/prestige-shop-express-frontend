"""
Script pour vérifier que le backend charge correctement les variables d'environnement
"""
import os
try:
    from dotenv import load_dotenv
except Exception:
    def load_dotenv(*args, **kwargs):
        return False

def verifier_variables():
    """Vérifier les variables d'environnement du backend"""
    print("🔍 Vérification des variables d'environnement pour le backend...")
    print("=" * 60)
    
    # Charger les variables depuis .env (silencieusement si python-dotenv est absent)
    load_dotenv()
    
    # Vérifier les variables
    gmail_address = os.environ.get('GMAIL_ADDRESS')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    print(f"📧 GMAIL_ADDRESS: {gmail_address if gmail_address else '❌ NON TROUVÉE'}")
    print(f"🔑 GMAIL_APP_PASSWORD: {'✅ PRÉSENTE' if gmail_password else '❌ NON TROUVÉE'}")
    
    if gmail_address and gmail_password:
        print("\n✅ Configuration complète pour le backend")
        print("   Vous pouvez maintenant lancer le serveur backend")
    else:
        print("\n❌ Configuration incomplète")
        print("   Vérifiez votre fichier .env")
    
    return gmail_address and gmail_password

if __name__ == "__main__":
    verifier_variables()