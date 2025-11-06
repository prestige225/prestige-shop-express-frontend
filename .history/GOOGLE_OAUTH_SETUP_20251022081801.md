# 🌐 GOOGLE OAUTH INTEGRATION - GUIDE DE CONFIGURATION

## ✅ ÉTAPES POUR CONFIGURER L'AUTHENTIFICATION GOOGLE

### Étape 1: Créer un projet Google Cloud

1. **Allez sur la console Google Cloud**
   - URL: https://console.cloud.google.com/
   - Connectez-vous avec votre compte Google

2. **Créez un nouveau projet**
   - Cliquez sur le sélecteur de projet (en haut)
   - Cliquez sur "Nouveau projet"
   - Nommez-le "PrestigeShop" ou un nom similaire
   - Cliquez sur "Créer"

3. **Activez l'API Google+**
   - Dans le menu, allez à "API et services" > "Bibliothèque"
   - Recherchez "Google+ API"
   - Cliquez dessus et cliquez sur "Activer"

### Étape 2: Créer les identifiants OAuth

1. **Allez à "API et services" > "Identifiants"**

2. **Cliquez sur "Créer des identifiants" > "ID client OAuth"**

3. **Configurez l'application**
   - Type d'application: "Application Web"
   - Nom: "PrestigeShop Web Client"

4. **Ajoutez les URI de redirection autorisées**
   ```
   http://localhost:5000/api/auth/google/callback
   http://127.0.0.1:5000/api/auth/google/callback
   ```

5. **Cliquez sur "Créer"**

6. **Notez vos identifiants**
   - **ID client**: Copiez cette valeur
   - **Clé secrète client**: Copiez cette valeur

### Étape 3: Mettre à jour le code serveur

Dans le fichier `server_fixed.py`, remplacez les valeurs suivantes:

```python
# Configuration Google OAuth
GOOGLE_CLIENT_ID = 'VOTRE_ID_CLIENT_ICI'
GOOGLE_CLIENT_SECRET = 'VOTRE_CLE_SECRETE_ICI'
GOOGLE_REDIRECT_URI = 'http://localhost:5000/api/auth/google/callback'
```

### Étape 4: Mettre à jour les pages HTML

#### Dans `login.html` et `register.html`:

Ajoutez le script Google Platform:
```html
<!-- Ajoutez ceci dans la section <head> -->
<script src="https://accounts.google.com/gsi/client" async defer></script>
```

Mettez à jour les boutons Google:
```html
<!-- Remplacez le bouton Google existant par: -->
<button onclick="loginWithGoogle()" class="flex items-center justify-center px-4 py-3 border-2 border-gray-200 rounded-xl hover:bg-gray-50 hover:border-gray-300 transition-all">
    <i class="fab fa-google text-red-500 text-xl mr-2"></i>
    <span class="font-semibold text-gray-700">Continuer avec Google</span>
</button>
```

Ajoutez le script JavaScript:
```html
<script>
// ========== GOOGLE AUTHENTICATION ==========
function loginWithGoogle() {
    // Rediriger vers le point de terminaison Google OAuth
    window.location.href = 'http://localhost:5000/api/auth/google';
}

// Vérifier si l'authentification Google a réussi
window.addEventListener('DOMContentLoaded', function() {
    const urlParams = new URLSearchParams(window.location.search);
    const googleError = urlParams.get('google_error');
    const googleSuccess = urlParams.get('google_success');
    
    if (googleError) {
        showError(decodeURIComponent(googleError));
    }
    
    if (googleSuccess) {
        showSuccess('Connexion avec Google réussie ! Redirection...');
        setTimeout(() => {
            window.location.href = 'index.html';
        }, 1500);
    }
});

function showError(message) {
    const errorDiv = document.getElementById('error-message') || document.createElement('div');
    const errorText = document.getElementById('error-text') || document.createElement('span');
    
    errorText.textContent = message;
    errorDiv.id = 'error-message';
    errorDiv.className = 'bg-red-50 border-l-4 border-red-500 text-red-700 p-4 rounded-lg';
    errorDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-exclamation-circle mr-2"></i>
            <span id="error-text">${message}</span>
        </div>
    `;
    
    // Ajouter à la fin du formulaire ou au début du body
    const form = document.getElementById('login-form') || document.getElementById('register-form');
    if (form) {
        form.parentNode.insertBefore(errorDiv, form.nextSibling);
    }
}

function showSuccess(message) {
    const successDiv = document.getElementById('success-message') || document.createElement('div');
    const successText = document.getElementById('success-text') || document.createElement('span');
    
    successText.textContent = message;
    successDiv.id = 'success-message';
    successDiv.className = 'bg-green-50 border-l-4 border-green-500 text-green-700 p-4 rounded-lg';
    successDiv.innerHTML = `
        <div class="flex items-center">
            <i class="fas fa-check-circle mr-2"></i>
            <span id="success-text">${message}</span>
        </div>
    `;
    
    // Ajouter à la fin du formulaire ou au début du body
    const form = document.getElementById('login-form') || document.getElementById('register-form');
    if (form) {
        form.parentNode.insertBefore(successDiv, form.nextSibling);
    }
}
</script>
```

### Étape 5: Tester l'authentification

1. **Démarrez votre serveur Flask**
   ```bash
   python server_fixed.py
   ```

2. **Ouvrez votre navigateur**
   - Allez sur `http://localhost:5000/login.html`
   - Cliquez sur le bouton "Continuer avec Google"
   - Connectez-vous avec un compte Google
   - Vous devriez être redirigé vers votre site

### Étape 6: Personnalisation (optionnel)

#### Pour une meilleure expérience utilisateur:

1. **Ajoutez une image de profil** (si disponible)
2. **Stockez les préférences utilisateur**
3. **Synchronisez les contacts Google** (optionnel)

### 🔧 DÉPANNAGE

#### Problèmes courants:

1. **"redirect_uri_mismatch"**
   - Vérifiez que vos URI de redirection dans Google Cloud correspondent exactement
   - Incluez à la fois `localhost` et `127.0.0.1`

2. **"invalid_client"**
   - Vérifiez que votre ID client et clé secrète sont corrects
   - Assurez-vous de ne pas avoir de caractères supplémentaires

3. **"access_denied"**
   - L'utilisateur a refusé l'autorisation
   - Réessayez et acceptez les permissions

4. **Problèmes de CORS**
   - Assurez-vous que CORS est correctement configuré dans Flask

### 🛡️ SÉCURITÉ

#### Bonnes pratiques:

1. **Ne partagez jamais vos clés secrètes**
2. **Utilisez HTTPS en production**
3. **Validez toujours les données reçues de Google**
4. **Stockez les tokens de manière sécurisée**
5. **Implémentez une expiration de session**

### 📊 DONNÉES UTILISATEUR

#### Informations récupérées via Google OAuth:

- Email (obligatoire)
- Nom de famille (family_name)
- Prénom (given_name)
- ID Google (sub)
- Photo de profil (picture) - optionnel

#### Données stockées dans la base de données:

```sql
-- Pour les utilisateurs Google, les champs seront:
nom = family_name
prenom = given_name
email = email
numero = '' (vide)
mot_de_passe = '' (vide - pas de mot de passe pour Google)
statut = 'actif'
```

### 🎯 FONCTIONNALITÉS SUPPLÉMENTAIRES

#### Vous pouvez étendre cette intégration:

1. **Synchronisation des contacts**
2. **Importation du calendrier**
3. **Partage de contenu**
4. **Notifications push**

### 📞 SUPPORT

En cas de problème:

1. **Vérifiez les logs du serveur Flask**
2. **Consultez la console du navigateur**
3. **Vérifiez les erreurs réseau**
4. **Assurez-vous que toutes les dépendances sont installées**

```bash
pip install -r requirements.txt
```

---

## ✅ RÉSUMÉ DES MODIFICATIONS

### Fichiers modifiés:

1. **`server_fixed.py`** - Ajout des routes Google OAuth
2. **`login.html`** - Bouton Google + script
3. **`register.html`** - Bouton Google + script
4. **`requirements.txt`** - Ajout de `requests`

### Nouvelles routes API:

- `GET /api/auth/google` - Initie l'authentification
- `GET /api/auth/google/callback` - Gère le retour OAuth

### Nouvelles dépendances:

- `requests==2.31.0` - Pour les appels API à Google

---

🎉 **Votre site est maintenant prêt pour l'authentification Google !**

Suivez ce guide étape par étape et vous aurez une intégration complète et sécurisée.