# 🔧 Dépannage - Erreurs API

## 🚨 Problème : "Le serveur API n'est pas accessible"

### Message d'erreur complet
```
Erreur de chargement
Le serveur API n'est pas accessible. Vérifiez votre connexion Internet.

Endpoint: https://prestige-shop-backend.onrender.com/api
```

---

## ✅ Solutions immédiates (depuis la page d'erreur)

### 1️⃣ **Recharger la page**
Cliquez sur le bouton **"Recharger la page"**

- Rafraîchit la connexion
- Réessaie automatiquement
- Solutionne les problèmes temporaires de réseau

---

### 2️⃣ **Essayer le serveur de secours**
Cliquez sur le bouton **"Essayer le serveur de secours"**

**Ce que ça fait :**
- Bascule automatiquement vers l'API de fallback
- Teste la connexion alternative
- Peut fonctionner si l'API principale est en panne

**Exemple :**
```
API Principale : https://prestige-shop-backend.onrender.com/api ❌
↓
API de Secours : http://localhost:5000/api ✅
```

---

### 3️⃣ **Tester l'API**
Cliquez sur le bouton **"Tester l'API"**

**Résultats possibles :**

✅ **En ligne** - L'API fonctionne  
⚠️ **Accessible mais erreur** - L'API répond mais avec une erreur  
❌ **Hors ligne** - L'API ne répond pas

**Utilité :**
- Diagnostiquer quelle API est en panne
- Savoir si c'est un problème local ou serveur
- Identifier la meilleure connexion

---

## 🔍 Diagnostics avancés

### Informations techniques affichées

La page d'erreur montre :

```
📊 Informations techniques :
API principale : https://prestige-shop-backend.onrender.com/api
API de secours : http://localhost:5000/api
Hôte : prestige-shop-express.onrender.com
Erreur : Failed to fetch
```

### Interprétation

| Information | Signification | Action |
|-------------|---------------|--------|
| `Failed to fetch` | Connexion réseau impossible | Vérifier Internet |
| `Timeout` | Serveur trop lent (>5s) | Réessayer plus tard |
| `404` | Endpoint inexistant | Vérifier l'URL |
| `500` | Erreur serveur | Contacter le support |

---

## 🛠️ Solutions selon le contexte

### Cas 1 : Vous êtes en PRODUCTION (Render)

**Symptômes :**
- Hôte : `prestige-shop-express.onrender.com`
- API principale : `https://prestige-shop-backend.onrender.com/api`

**Solutions :**

#### A. Le backend Render est endormi
```bash
# Solution : Réveiller le backend
curl https://prestige-shop-backend.onrender.com/health
```

**Attendez 30 secondes** et rafraîchissez la page.

---

#### B. Le backend est planté
**Vérification :**
```bash
curl https://prestige-shop-backend.onrender.com/ping
```

**Si erreur :**
1. Allez sur le dashboard Render
2. Redémarrez le service backend
3. Attendez 1-2 minutes
4. Rafraîchissez la page

---

#### C. Problème de CORS
**Dans la console navigateur (F12) :**
```
Access to fetch at '...' from origin '...' has been blocked by CORS policy
```

**Solution :**
- Vider le cache du navigateur (`Ctrl + Shift + Suppr`)
- Réessayer dans 10 minutes (le temps que CORS se propage)

---

### Cas 2 : Vous êtes en LOCAL

**Symptômes :**
- Hôte : `localhost` ou `127.0.0.1`
- API principale : `http://localhost:5000/api`

**Solutions :**

#### A. Le serveur Flask n'est pas lancé
**Vérification :**
```bash
# Dans un terminal
curl http://localhost:5000/ping
```

**Si échec :**
```bash
# Démarrer le serveur
cd "c:\Users\RCK COMPUTERS\Desktop\prestige shop express"
python backend_render/server_fixed.py
```

**Message attendu :**
```
 * Running on http://127.0.0.1:5000
 * Running on http://XXX.XXX.X.XX:5000
```

---

#### B. Port déjà utilisé
**Erreur :**
```
OSError: [WinError 10048] Only one usage of each socket address is normally allowed
```

**Solution :**
```bash
# Trouver le processus utilisant le port 5000
netstat -ano | findstr :5000

# Tuer le processus (remplacer PID par le vrai numéro)
taskkill /PID <PID> /F

# Ou utiliser un autre port
python app.py --port 5001
```

---

#### C. Fallback vers production
Si votre serveur local ne marche pas :

1. Cliquez sur **"Essayer le serveur de secours"**
2. Ça basculera sur `https://prestige-shop-backend.onrender.com/api`
3. Utile pour tester sans le backend local

---

## ⚡ Correctifs rapides

### Pour les développeurs

#### 1. **Vérifier la configuration API**

Dans `index.html`, lignes ~5367-5390 :

```javascript
(function() {
    const hostname = window.location.hostname;
    
    if (hostname.includes('onrender.com')) {
        window.API_BASE_URL = 'https://prestige-shop-backend.onrender.com/api';
        window.API_FALLBACK_URL = 'http://localhost:5000/api';
    } else if (hostname === 'localhost') {
        window.API_BASE_URL = 'http://localhost:5000/api';
        window.API_FALLBACK_URL = 'https://prestige-shop-backend.onrender.com/api';
    }
})();
```

**Vérifiez que :**
- ✅ Les URLs sont correctes
- ✅ Le hostname correspond à votre environnement
- ✅ Les deux URLs sont configurées (principale + fallback)

---

#### 2. **Ajouter un endpoint de test**

Dans `backend_render/server_fixed.py` :

```python
@app.route('/api/test', methods=['GET'])
def test():
    return jsonify({
        'status': 'ok',
        'timestamp': datetime.now().isoformat(),
        'service': 'prestige-shop-backend'
    })
```

**Utilité :**
- Tester rapidement l'API
- Vérifier la connectivité
- Mesurer le temps de réponse

---

#### 3. **Améliorer les logs**

Dans la console du navigateur (F12), ajoutez :

```javascript
// Activer les logs détaillés
localStorage.setItem('debug_api', 'true');

// Recharger la page
location.reload();
```

**Résultat :**
- Logs détaillés dans la console
- Traces des requêtes HTTP
- Debug facilité

---

## 📊 Tableau de décision

| Symptôme | Cause probable | Solution |
|----------|----------------|----------|
| "Failed to fetch" | Réseau coupé | Vérifier connexion Internet |
| Timeout (>5s) | Serveur lent | Attendre 30s, réessayer |
| 404 Not Found | Mauvaise URL | Vérifier endpoint dans `index.html` |
| 500 Server Error | Bug backend | Redémarrer serveur, check logs |
| CORS Error | Configuration CORS | Vider cache, attendre propagation |
| ERR_CONNECTION_REFUSED | Serveur éteint | Démarrer serveur Flask |

---

## 🔄 Procédure de redémarrage complète

### En production (Render)

```bash
# 1. Redémarrer le backend
# Via dashboard Render ou CLI
render services restart prestige-shop-backend

# 2. Attendre 2 minutes
sleep 120

# 3. Tester la santé
curl https://prestige-shop-backend.onrender.com/health

# 4. Rafraîchir le frontend
# Via dashboard Render ou Git push
git commit --allow-empty -m "Redeploy"
git push origin main
```

### En local (Windows)

```powershell
# 1. Tuer tous les processus Python
Get-Process python | Stop-Process -Force

# 2. Nettoyer les ports
netstat -ano | findstr :5000
# (noter le PID et le tuer si nécessaire)

# 3. Redémarrer proprement
cd "c:\Users\RCK COMPUTERS\Desktop\prestige shop express"
python backend_render/server_fixed.py

# 4. Dans un autre terminal, tester
curl http://localhost:5000/ping
```

---

## 🆘 Support

### Si rien ne fonctionne

1. **Vérifier l'état des services Render**
   - https://status.render.com/

2. **Consulter les logs**
   ```bash
   # Backend Render
   render logs -f -s prestige-shop-backend
   
   # Local (dans le terminal où tourne Flask)
   # Regarder les erreurs directement
   ```

3. **Contacter le support**
   - Email : support@prestige-shop.com
   - Inclure :
     - Capture d'écran de l page d'erreur
     - Logs de la console (F12)
     - Résultats des tests API

---

## 🎯 Prévention

### Bonnes pratiques

1. **Toujours avoir un fallback**
   - Configurer `API_FALLBACK_URL`
   - Tester régulièrement le basculement

2. **Monitoring**
   - Utiliser un service comme UptimeRobot
   - Alerts automatiques si API down

3. **Cache intelligent**
   ```javascript
   // Dans index.html
   const cachedProducts = localStorage.getItem('cachedProducts');
   if (cachedProducts && apiIsDown()) {
       // Afficher le cache même si API down
       displayProducts(JSON.parse(cachedProducts));
   }
   ```

4. **Health checks réguliers**
   ```javascript
   // Toutes les 5 minutes
   setInterval(() => {
       fetch(`${API_BASE_URL}/ping`)
           .then(r => r.ok ? console.log('✅ API OK') : console.log('❌ API DOWN'));
   }, 300000);
   ```

---

## 📝 Checklist de résolution

Quand vous avez une erreur API :

- [ ] 1. Cliquer sur **"Recharger la page"**
- [ ] 2. Si échec, cliquer sur **"Essayer le serveur de secours"**
- [ ] 3. Si échec, cliquer sur **"Tester l'API"**
- [ ] 4. Lire les **informations techniques**
- [ ] 5. Identifier la cause (réseau, serveur, CORS, etc.)
- [ ] 6. Appliquer la solution appropriée
- [ ] 7. Si toujours bloqué, **contacter le support**

---

**Document créé pour Prestige Shop Express**  
*Version 1.0 - Mars 2026*  
*Mis à jour : Ajout fonctions tryFallbackAPI() et checkAPIStatus()*
