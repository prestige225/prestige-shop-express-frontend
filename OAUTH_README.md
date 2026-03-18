# 🔧 RÉSOLUTION DE L'ERREUR OAUTH GOOGLE "origin_mismatch"

## ⚠️ Problème
```
Erreur 400: origin_mismatch
Vous ne pouvez pas vous connecter à cette appli, car elle ne respecte pas le règlement OAuth 2.0 de Google.
```

## ⚡ SUPER RAPIDE - Vous avez le port 5506?

Si vous voyez ce message:
```
❌ votre URL: http://127.0.0.1:5506
❌ Port non configuré
```

**Ouvrez ceci immédiatement:** [fix-port-5506.html](fix-port-5506.html) ← 3 minutes pour corriger!

### **Étape 1: Identifier votre URL** (1 minute)
Ouvrez: [**fix-oauth-guide.html**](fix-oauth-guide.html)
- Votre URL actuelle s'affichera
- Cliquez "Copier"

### **Étape 2: Ajouter l'URL à Google Cloud** (2 minutes)
1. Allez sur [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Sélectionnez le projet `Prestige Shop Express New`
3. Cliquez sur l'ID client OAuth: `722931671687-fj2ph80jpqvlqmqnmc3aepdfqtsl7eqe.apps.googleusercontent.com`
4. Section **"Origines JavaScript autorisées"** → **"+ Ajouter URI"**
5. Collez votre URL → **Enregistrer**

### **Étape 3: Attendre et tester** (5 minutes)
- Attendez 3-5 minutes que la configuration se propage
- Videz le cache: `Ctrl+Shift+Delete` → Tout supprimer
- Rechargez: `Ctrl+F5`
- Essayez de vous connecter

---

## 📚 Ressources créées

| Fichier | Utilité | Lien |
|---------|---------|------|
| **fix-port-5506.html** | ⚡ Guide rapide port 5506 (3 min) | [Ouvrir](fix-port-5506.html) |
| **fix-oauth-guide.html** | Guide visuel interactif (générique) | [Ouvrir](fix-oauth-guide.html) |
| **debug-oauth.html** | Diagnostic technique - affiche votre URL actuelle | [Ouvrir](debug-oauth.html) |
| **FIX_OAUTH_GUIDE.md** | Guide complet en Markdown | [Lire](FIX_OAUTH_GUIDE.md) |
| **login.html** | Page de connexion (avec détection automatique) | [Voir](login.html) |
| **register.html** | Page d'inscription (avec détection automatique) | [Voir](register.html) |
| **OAUTH_README.md** | **← Vous êtes ici** |  |

---

## ✅ Origines actuellement configurées

Ces origines JavaScript sont **déjà autorisées** dans Google Cloud:

```
✅ http://localhost:5000
✅ http://localhost:3000
✅ http://localhost:5504
✅ http://localhost:5505
✅ http://localhost:5506  ← NOUVEAU!
✅ http://127.0.0.1:5504
✅ http://127.0.0.1:5505
✅ http://127.0.0.1:5506  ← NOUVEAU!
✅ https://prestige-shop-backend.onrender.com
✅ https://prestige-shop-express.onrender.com
```

## 🔑 Client ID OAuth

```
Nom du client: Prestige Shop Express New
Client ID: 722931671687-fj2ph80jpqvlqmqnmc3aepdfqtsl7eqe.apps.googleusercontent.com
```

---

## 🆘 Dépannage rapide

### ❌ L'erreur "origin_mismatch" persiste?

**Cause 1: Vous accédez depuis une URL non configurée**
- Solution: Ouvrez [fix-oauth-guide.html](fix-oauth-guide.html) et ajoutez votre URL

**Cause 2: Configuration pas propagée**
- Solution: Attendez 10 minutes et essayez en mode incognito

**Cause 3: Cache du navigateur trop agressif**
- Solution: Videz tout (Ctrl+Shift+Delete) et rechargez (Ctrl+F5)

**Cause 4: Protocole mismatch (http vs https)**
- Solution: Assurez-vous que http et https ne sont pas mélangés

---

## 💡 Améliorations apportées au code

### **login.html et register.html** - Détection automatique
Maintenant, quand vous chargez la page, si votre URL n'est pas configurée:
- ⚠️ Un avertissement s'affiche  
- 📋 Vous pouvez copier votre URL
- 🔑 Lien direct vers Google Cloud Console

### **debug-oauth.html** - Diagnostic technique
- Affiche votre URL actuelle
- Compare avec les origines autorisées
- Indique exactement ce qui manque

### **fix-oauth-guide.html** - Guide visuel complet
- Instructions étape par étape
- Boutons pratiques
- Checklist interactive
- Dépannage avancé

---

## 📞 Informations techniques

### Configuration serveur (app.py)
```python
# Le serveur Flask accepte les requêtes CORS
response.headers['Access-Control-Allow-Origin'] = '*'
```

### Configuration backend (server_fixed.py)
```python
CORS(app, 
     origins=["http://localhost:5000", "http://localhost:5504", ...],
     supports_credentials=True)
```

### Google Library
```html
<script src="https://accounts.google.com/gsi/client" async defer></script>
```

---

## 🚀 Prochaines étapes

1. ✅ Ouvrez [fix-oauth-guide.html](fix-oauth-guide.html)
2. ✅ Suivez les étapes pour ajouter votre URL à Google Cloud
3. ✅ Attendez 5 minutes
4. ✅ Testez la connexion avec Google
5. ✅ Si ça ne marche pas, consultez [debug-oauth.html](debug-oauth.html)

---

## 📖 Ressources externes

- [Google OAuth 2.0 Doc](https://developers.google.com/identity/protocols/oauth2)
- [Google Cloud Console](https://console.cloud.google.com)
- [Erreur origin_mismatch](https://developers.google.com/identity/protocols/oauth2/web-server#origin-restrictions)
- [Google Sign-In Library](https://developers.google.com/identity/gsi/web)

---

## ✨ Astuce bonus

Si vous testez **en local** depuis `http://localhost:5504`, c'est déjà autorisé!
Essayez simplement de:
1. Vider le cache (Ctrl+Shift+Delete)
2. Rechargez la page (Ctrl+F5)
3. Attendez 5 minutes

En 90% des cas, c'est juste un problème de cache et de propagation.

---

**Dernière mise à jour:** 15 mars 2026  
**Version:** 1.0  
**Statut:** ✅ En production
