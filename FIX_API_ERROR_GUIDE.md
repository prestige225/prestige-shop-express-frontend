# 🔧 Guide de Débogage des Erreurs API

## Problèmes Identifiés

### 1. Erreur 405 (Method Not Allowed)
**Symptôme:** 
```
POST https://prestige-shop-express.onrender.com/api/register 405 (Method Not Allowed)
POST https://prestige-shop-express.onrender.com/api/auth/google/callback/web 405 (Method Not Allowed)
```

**Causes possibles:**
- Le serveur ne reconnaît pas la route
- Problème de configuration CORS
- Les en-têtes de la requête sont incorrects

**Solutions appliquées:**
1. ✅ Ajout des gestionnaires d'erreur JSON (au lieu de HTML)
2. ✅ Middleware de logging pour tracer toutes les requêtes
3. ✅ En-têtes CORS automatiques sur toutes les réponses
4. ✅ Configuration de session améliorée

### 2. Erreur "Unexpected token '<', "<!doctype "..."
**Symptôme:**
```
SyntaxError: Unexpected token '<', "<!doctype "... is not valid JSON
```

**Cause:** Le serveur retourne une page HTML (page d'erreur Flask) au lieu d'une réponse JSON.

**Solution:** 
- Les gestionnaires d'erreur 404/405/500 retournent maintenant du JSON
- Toutes les exceptions sont capturées et retournent du JSON

### 3. Problèmes Google OAuth
**Symptôme:**
```
Failed to render button because there is no parent or options set
FedCM get() rejects with NetworkError
Cross-Origin-Opener-Policy policy would block the window.postMessage call
```

**Causes:**
- Configuration Google OAuth incorrecte dans Google Cloud Console
- Problème de domaine autorisé
- Headers COOP/COEP manquants

**Solutions:**
1. Vérifier que le domaine `https://prestige-shop-express.onrender.com` est bien configuré dans Google Cloud Console
2. Ajouter les URLs autorisées dans les paramètres OAuth
3. Utiliser `SESSION_COOKIE_SAMESITE='Lax'` au lieu de `'None'`

## 📋 Comment Tester

### Test 1: Utiliser la page de test API
Ouvrez `test-api-routes.html` dans votre navigateur et cliquez sur les boutons de test.

### Test 2: Vérifier les logs du serveur
Les logs détaillés montrent maintenant:
- La méthode HTTP
- Le chemin de la requête
- L'origine de la requête
- Les en-têtes
- Les cookies

### Test 3: Inscription manuelle
1. Ouvrez `register.html`
2. Remplissez le formulaire avec des données de test
3. Ouvrez la console (F12) pour voir les logs détaillés

## 🔍 Logs à Surveiller

### Côté Client (Navigateur):
```javascript
console.log('🔧 Backend PRODUCTION activé:', API_BASE_URL);
console.log('Envoi des données d\'inscription:', {...});
console.log('Réponse HTTP complète:', response);
```

### Côté Serveur (Render):
```
📥 Requête reçue: POST /api/register
🌐 Origine: https://prestige-shop-express.onrender.com
📋 Content-Type: application/json
📤 Headers: {...}
```

## ⚙️ Configuration Requise

### Variables d'Environnement (Render):
```bash
DB_HOST=bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com
DB_USER=usblj9n0kraq8uoc
DB_PASSWORD=4fcY691gsJlwoQnk5xwa
DB_NAME=bracv1wswmu4vsqxycku
DB_PORT=3306
SECRET_KEY=votre_clé_secrète_ici
GOOGLE_CLIENT_ID=722931671687-fj2ph80jpqvlqmqnmc3aepdfqtsl7eqe.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=GOCSPX-...
PORT=5000 (ou celui fourni par Render)
```

### Google Cloud Console:
Ajoutez ces URLs dans "Authorized JavaScript origins":
- `https://prestige-shop-express.onrender.com`
- `http://localhost:5504` (développement)
- `http://localhost:5505` (développement)

Ajoutez ces URLs dans "Authorized redirect URIs":
- `https://prestige-shop-express.onrender.com/login.html`
- `http://localhost:5504/login.html`
- `http://localhost:5505/login.html`

## 🚀 Déploiement

Après avoir poussé les modifications sur GitHub:
1. Render va automatiquement redéployer
2. Attendez que le déploiement soit complet (~2-3 minutes)
3. Testez avec `test-api-routes.html`
4. Vérifiez les logs sur Render Dashboard

## 📊 Vérification du Succès

Une requête réussie doit retourner:
```json
{
  "success": true,
  "message": "...",
  ...
}
```

Avec un status HTTP 200 ou 201.

## ❌ Si Ça Ne Marche Toujours Pas

1. **Vérifiez les logs Render:**
   - Allez sur Render Dashboard
   - Cliquez sur votre service
   - Onglet "Logs"
   - Cherchez les erreurs avec ❌

2. **Testez en local:**
   ```bash
   cd backend_render
   python server_fixed.py
   ```
   Puis ouvrez `http://localhost:5000/test-api-routes.html`

3. **Vérifiez la base de données:**
   - La table `users` existe-t-elle ?
   - Les colonnes correspondent-elles aux champs utilisés ?

4. **Contactez le support:**
   - Fournissez les logs complets
   - Incluez les captures d'écran des erreurs
   - Précisez l'URL exacte qui pose problème

## 🛠️ Fichiers Modifiés

- `backend_render/server_fixed.py`: Gestionnaires d'erreur, logging, CORS
- `test-api-routes.html`: Page de test ajoutée
- Configuration de session améliorée

## 📝 Notes Importantes

- **Ne jamais utiliser `&&` dans PowerShell** (utiliser `;` ou point-virgule)
- **Toujours tester en local avant de déployer**
- **Garder les logs activés en production pour le débogage**
- **Changer `SESSION_COOKIE_SECURE` à `True` quand HTTPS est activé**
