"""
Test simple d'envoi d'email avec Gmail
"""
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def test_envoi_simple():
    """Test d'envoi d'email simple"""
    print("🧪 Test d'envoi d'email simple...")
    
    # Récupérer les identifiants
    gmail_address = os.environ.get('GMAIL_ADDRESS')
    gmail_password = os.environ.get('GMAIL_APP_PASSWORD')
    
    if not gmail_address or not gmail_password:
        print("❌ Variables d'environnement manquantes")
        print("Configurez:")
        print("$env:GMAIL_ADDRESS='votre_email@gmail.com'")
        print("$env:GMAIL_APP_PASSWORD='mot_de_passe_application'")
        return False
    
    try:
        print(f"📧 Tentative d'envoi depuis {gmail_address}")
        
        # Créer le message
        msg = MIMEMultipart()
        msg['From'] = gmail_address
        msg['To'] = gmail_address  # Envoyer à soi-même pour test
        msg['Subject'] = "Test Email Local"
        body = "Ceci est un test d'envoi d'email local."
        msg.attach(MIMEText(body, 'plain'))
        
        # Connexion et envoi
        print("🔗 Connexion au serveur Gmail...")
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(gmail_address, gmail_password)
        
        print("📤 Envoi de l'email...")
        text = msg.as_string()
        server.sendmail(gmail_address, gmail_address, text)
        server.quit()
        
        print("✅ Email envoyé avec succès!")
        return True
        
    except smtplib.SMTPAuthenticationError as e:
        print(f"❌ Erreur d'authentification: {e}")
        print("Solutions possibles:")
        print("1. Vérifiez que le mot de passe est correct")
        print("2. Activez la validation en 2 étapes")
        print("3. Générez un nouveau mot de passe d'application")
        return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

if __name__ == "__main__":
    test_envoi_simple()