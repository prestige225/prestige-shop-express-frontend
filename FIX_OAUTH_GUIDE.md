# 🔧 GUIDE DE CORRECTION - Erreur OAuth Google "origin_mismatch"

## Problème
```
Erreur 400: origin_mismatch
Vous ne pouvez pas vous connecter à cette appli, car elle ne respecte pas le règlement OAuth 2.0 de Google.
Si vous êtes le développeur de l'appli, enregistrez l'origine JavaScript dans la console Google Cloud.
```

---

## 🎯 Solution RAPIDE (5 minutes)

### ÉTAPE 1: Identifier votre URL actuelle
Ouvrez: `http://localhost:5000/debug-oauth.html` ou votre URL réelle
- Notez l'**Origine** affichée (par exemple: `http://localhost:5504`)

### ÉTAPE 2: Aller à Google Cloud Console
1. Accédez à: https://console.cloud.google.com/apis/credentials
2. Connectez-vous avec vos identifiants Google
3. Sélectionnez votre projet "Prestige Shop Express New"
4. Cliquez sur **l'ID client OAuth** (722931671687-fj2ph80jpqvlqmqnmc3aepdfqtsl7eqe)

### ÉTAPE 3: Ajouter votre Origine
1. Scrollez à **"Origines JavaScript autorisées"**
2. Cliquez sur **"+ Ajouter URI"**
3. Collez votre origine (copiée à l'étape 1)
4. Cliquez **"Enregistrer"**

### ÉTAPE 4: Attendez et testez
- Attendez **3-5 minutes** avant de tester (propagation)
- Videz le cache: **Ctrl+Shift+Delete** → Cache/Cookies → Tout supprimer
- Rechargez la page: **Ctrl+F5**
- Testez l'authentification Google

---

## 💡 ORIGINES QUI SONT ACTUELLEMENT AUTORISÉES

| Origine | Status |
|---------|--------|
| `http://localhost:5000` | ✅ Configuré |
| `http://localhost:3000` | ✅ Configuré |
| `http://127.0.0.1:5504` | ✅ Configuré |
| `http://localhost:5504` | ⚠️ À ajouter |
| `http://localhost:5505` | ⚠️ À ajouter |
| `https://prestige-shop-backend.onrender.com` | ✅ Configuré |
| `https://prestige-shop-express.onrender.com` | ✅ Configuré |
| `http://127.0.0.1:5505` | ✅ Configuré |

---

## 🔍 Causes les plus courantes

### ❌ Cause 1: Accès depuis une URL non configurée
```
Exemple: Vous accédez depuis http://localhost:8000, mais ce port n'est pas ajouté
Solution: Ajouter http://localhost:8000 aux origines JavaScript
```

### ❌ Cause 2: Confusion http/https
```
Exemple: Configuré comme https://prestige-shop-express.onrender.com
Mais accédé depuis: http://prestige-shop-express.onrender.com
Solution: S'assurer que le protocole (http vs https) correspond
```

### ❌ Cause 3: Port manquant
```
Exemple: Configuré comme http://localhost:5000
Mais accédé depuis: http://localhost:5504
Solution: Ajouter tous les ports que vous utilisez
```

### ❌ Cause 4: Configuration non propagée
```
Symptôme: Ajout fait récemment, mais erreur persiste
Solution: Attendre 5-10 minutes et vider le cache du navigateur
```

---

## ✅ Procédures recommandées

### Pour le DÉVELOPPEMENT LOCAL

**Assurez-vous que ces origines sont configurées:**
```
http://localhost:5000
http://localhost:3000
http://localhost:5504
http://localhost:5505
http://localhost:5506
http://127.0.0.1:5504
http://127.0.0.1:5505
http://127.0.0.1:5506
```

### Pour la PRODUCTION

**Assurez-vous que ces origines sont configurées:**
```
https://prestige-shop-express.onrender.com
https://prestige-shop-backend.onrender.com
https://adminprestigeshopexpress.onrender.com
```

---

## 🛠️ Solutions techniques avancées

### Solution 1: Ajouter all'origine manquante au backend
Si vous contrôlez le backend, modifiez [server_fixed.py](server_fixed.py):

```python
CORS(app, 
     origins=[
         "http://localhost:5000",
         "http://localhost:3000",
         "http://localhost:5504",    # ← AJOUTER SI MANQUANT
         "http://localhost:5505",    # ← AJOUTER SI MANQUANT
         "http://127.0.0.1:5504",
         "http://127.0.0.1:5505",
         "https://prestige-shop-backend.onrender.com",
         "https://prestige-shop-express.onrender.com",
         "*"  # ← À restreindre en production
     ], 
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"], 
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True)
```

### Solution 2: Configuration dynamique

Si vous détectez qu'l'origine n'est pas configurée, ajoutez-la automatiquement:

```javascript
// Dans login.html
function detectAndAddOrigin() {
    const currentOrigin = window.location.origin;
    const authorizedOrigins = [
        'http://localhost:5000',
        'http://localhost:3000',
        'http://127.0.0.1:5504',
        // ...
    ];
    
    if (!authorizedOrigins.includes(currentOrigin)) {
        console.warn(`⚠️ ATTENTION: Votre origine n'est pas configurée: ${currentOrigin}`);
        console.warn('Veuillez ajouter cette origine à Google Cloud Console');
        showOriginMismatchWarning(currentOrigin);
    }
}

function showOriginMismatchWarning(origin) {
    const warning = document.createElement('div');
    warning.style.cssText = 'background: #fff3cd; border: 1px solid #ff9800; padding: 15px; margin: 20px 0; border-radius: 4px;';
    warning.innerHTML = `
        <strong>⚠️ Erreur de configuration OAuth</strong><br/>
        Votre origine actualorique <code>${origin}</code> n'est pas configurée.<br/>
        <a href="https://console.cloud.google.com/apis/credentials" target="_blank">Aller à Google Cloud Console</a>
    `;
    document.body.insertBefore(warning, document.body.firstChild);
}

// Appeler au chargement
detectAndAddOrigin();
```

### Solution 3: Implémenter un proxy côté serveur

Si vous ne pouvez pas modifier Google Cloud Console, créez un proxy sur votre backend:

```python
# Dans server_fixed.py
@app.route('/auth/google-callback', methods=['POST'])
def google_callback_proxy():
    """Proxy pour gérer les réponses Google OAuth"""
    data = request.get_json()
    
    # Envoyer le token Google à Google pour validation
    # ... code de vérification du token ...
    
    return jsonify({
        'success': True,
        'user': {...}
    })
```

---

## 📋 Checklist avant de redémarrer

- [ ] J'ai identifié mon URL actuelle (copiée de debug-oauth.html)
- [ ] J'ai vérifié que cette URL est dans les origines JavaScript Google
- [ ] Si elle ne l'est pas, je l'ai ajoutée
- [ ] J'ai attendu 5 minutes pour la propagation
- [ ] J'ai vidé le cache du navigateur (Ctrl+Shift+Del)
- [ ] J'ai rechargé la page (Ctrl+F5)
- [ ] J'ai essayé dans une fenêtre incognito
- [ ] Le système fonctionne maintenant ✅

---

## 🆘 Si ça ne fonctionne toujours pas

1. **Vérifiez le client_id**
   - Dans [login.html](login.html#L406): `data-client_id="722931671687-fj2ph80jpqvlqmqnmc3aepdfqtsl7eqe.apps.googleusercontent.com"`
   - Confirmez que c'est le bon ID pour votre projet Google

2. **Vérifiez la console JavaScript**
   - Ouvrez F12 → Console
   - Cherchez des messages d'erreur détaillés
   - Signalez-les

3. **Testez avec des URLs alternatives**
   - Essayez `http://127.0.0.1:5504/login.html`
   - Essayez `http://localhost:5504/login.html`
   - Essayez la version Render: `https://prestige-shop-express.onrender.com/login.html`

4. **Réinitialisez les credentials Google**
   - Supprimez tous les tokens de session
   - Déconnectez-vous de votre compte Google
   - Reconnectez-vous

---

## 📞 Ressources utiles

- 📚 [Google OAuth 2.0 Documentation](https://developers.google.com/identity/protocols/oauth2)
- 🔑 [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
- 🐛 [Erreur origin_mismatch](https://developers.google.com/identity/protocols/oauth2/web-server#origin-restrictions)
- 💻 [Page de diagnostic locale](debug-oauth.html)
