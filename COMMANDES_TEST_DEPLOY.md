# 🚀 Commandes pour Tester et Déployer les Corrections

## 📋 Résumé Rapide

Votre serveur rencontre des erreurs 405 et retourne du HTML au lieu de JSON. Les corrections ont été appliquées dans `server_fixed.py`.

## 🔧 Étape 1: Tester en Local (Recommandé)

### Option A: Avec le script Python automatisé

```powershell
# Installer les dépendances si nécessaire
pip install requests colorama

# Lancer le serveur backend (dans un terminal)
cd backend_render
python server_fixed.py

# Dans un AUTRE terminal, lancer les tests
python test_api_local.py
```

### Option B: Manuellement avec le navigateur

```powershell
# Lancer le serveur backend
cd backend_render
python server_fixed.py
```

Puis ouvrez votre navigateur sur :
- `http://localhost:5000/test-api-routes.html`
- Cliquez sur les boutons de test

### Option C: Test rapide avec curl

```powershell
# Test endpoint /api/test
curl http://localhost:5000/api/test

# Test inscription
curl -X POST http://localhost:5000/api/register `
  -H "Content-Type: application/json" `
  -d "{\"nom\":\"Test\",\"prenom\":\"User\",\"email\":\"test@example.com\",\"mot_de_passe\":\"password123\"}"

# Test route inexistante (doit retourner JSON)
curl http://localhost:5000/api/route-inexistante
```

## ✅ Ce Que Vous Devez Voir

### Logs du Serveur (quand une requête arrive):
```
================================================================================
📥 Requête reçue: POST /api/register
🌐 Origine: http://localhost:5000
📋 Content-Type: application/json
🍪 Cookies: {}
📤 Headers: {...}
================================================================================
```

### Réponse Attendue (dans la console ou test_api_local.py):
```json
{
  "success": true,
  "message": "Utilisateur créé avec succès",
  "user_id": 123
}
```

## 🌐 Étape 2: Déployer sur Render

### Via Git (Automatique):

```powershell
# Ajouter les modifications
git add .

# Commit
git commit -m "FIX: Ajout gestionnaires d'erreur JSON et logging API"

# Push (Render va déployer automatiquement)
git push origin main
```

### Attendre le Déploiement:
1. Allez sur https://dashboard.render.com/
2. Cliquez sur "prestige-shop-express"
3. Surveillez les logs de déploiement (~2-3 minutes)
4. Attendez "✅ Deployed successfully"

## 🧪 Étape 3: Tester en Production

### Test 1: Page de Test
Ouvrez : `https://prestige-shop-express.onrender.com/test-api-routes.html`

### Test 2: Inscription Réelle
1. Ouvrez : `https://prestige-shop-express.onrender.com/register.html`
2. Remplissez le formulaire
3. Ouvrez la console (F12) pour voir les logs

### Test 3: Vérifier les Logs Render
1. Dashboard Render → prestige-shop-express → Logs
2. Cherchez les emojis 📥, ✅, ❌
3. Vérifiez que les réponses sont bien en JSON

## 🛠️ En Cas de Problème

### Le serveur ne démarre pas en local:
```powershell
# Vérifier les erreurs de syntaxe
python -m py_compile backend_render/server_fixed.py

# Vérifier les dépendances
pip install -r requirements.txt

# Lancer avec plus de logs
python backend_render/server_fixed.py 2>&1 | tee server.log
```

### Erreurs 405 persistent:
1. Vérifiez les logs Render pour voir quelle route est appelée
2. Comparez avec les routes définies dans `server_fixed.py`
3. Vérifiez que `api-config.js` est correct

### Toujours du HTML au lieu de JSON:
1. Vérifiez que les gestionnaires d'erreur sont bien dans `server_fixed.py`
2. Redémarrez le serveur
3. Videz le cache de votre navigateur (Ctrl+Shift+Suppr)

## 📊 Checklist de Vérification

- [ ] Le serveur local démarre sans erreur
- [ ] `/api/test` retourne du JSON
- [ ] `/api/register` accepte les POST
- [ ] Les erreurs 404 retournent du JSON
- [ ] Les logs montrent bien les requêtes entrantes
- [ ] Git push effectué
- [ ] Déploiement Render terminé
- [ ] Tests en production réussis

## 🎯 Résultat Final

Après ces corrections :
- ✅ Toutes les erreurs API retournent du JSON (plus de HTML)
- ✅ Les logs détaillés aident au débogage
- ✅ CORS fonctionne correctement
- ✅ Google OAuth devrait fonctionner (si bien configuré)

## 📞 Besoin d'Aide ?

Si vous avez toujours des problèmes :
1. Fournissez les logs complets du serveur
2. Incluez les captures d'écran des erreurs
3. Précisez si ça marche en local ou non
4. Donnez l'URL exacte qui pose problème

## 🔗 Fichiers Importants

- `backend_render/server_fixed.py` - Serveur corrigé
- `test-api-routes.html` - Page de test navigateur
- `test_api_local.py` - Script de test Python
- `FIX_API_ERROR_GUIDE.md` - Guide complet
- `RESUME_CORRECTIONS_API.md` - Résumé des changements

---

**Pro Tip:** Gardez toujours un terminal avec les logs du serveur ouvert pendant le développement pour voir les requêtes en temps réel !
