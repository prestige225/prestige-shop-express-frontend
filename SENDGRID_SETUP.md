# 📧 Configuration SendGrid pour l'envoi d'emails

## ✅ Étape 1 : Créer un compte SendGrid

1. Allez sur [https://sendgrid.com/](https://sendgrid.com/)
2. Cliquez sur **"Sign Up"** (inscription gratuite)
3. Remplissez le formulaire :
   - **Prénom/Nom** : Votre nom
   - **Email** : Un email personnel
   - **Mot de passe** : Créez un mot de passe fort
   - **Company** : Prestige Shop Express
4. Acceptez les conditions et créez le compte

**Avantages SendGrid gratuit :**
- ✅ 100 emails par jour (gratuit)
- ✅ Pas de limite de durée
- ✅ Interface intuitive
- ✅ API fiable et sécurisée

---

## ✅ Étape 2 : Obtenir la clé API SendGrid

1. Connectez-vous à [https://app.sendgrid.com/](https://app.sendgrid.com/)
2. Allez dans **Settings** → **API Keys**
3. Cliquez sur **Create API Key**
4. Remplissez :
   - **API Key Name** : `Prestige Shop Express`
   - **API Key Permissions** : Sélectionnez **"Restricted Access"**
   - Sous "Mail Send" : Cochez ✅ **Send**
5. Cliquez sur **Create & View**
6. **COPIEZ LA CLÉ** (vous ne pouvez la voir qu'une fois !)

**Format :** `SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

---

## ✅ Étape 3 : Configurer l'adresse d'envoi (From Email)

1. Dans SendGrid, allez dans **Settings** → **Sender Authentication**
2. Cliquez sur **Verify a Single Sender**
3. Remplissez :
   - **From Email Address** : `noreply@prestigeshopexpress.com` (ou votre domaine)
   - **From Name** : `Prestige Shop Express`
   - **Recipient Email** : Votre email
4. SendGrid vous enverra un email de vérification
5. Cliquez sur le lien de vérification

**Alternative :** Vous pouvez utiliser n'importe quel email au début, puis vérifier votre domaine plus tard.

---

## ✅ Étape 4 : Configurer les variables d'environnement sur Render

1. Allez sur le dashboard Render : [https://dashboard.render.com/](https://dashboard.render.com/)
2. Sélectionnez le service **prestige-shop-backend**
3. Cliquez sur **Environment**
4. Ajoutez les variables d'environnement :

```
SENDGRID_API_KEY = SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SENDGRID_FROM_EMAIL = noreply@prestigeshopexpress.com
SENDGRID_FROM_NAME = Prestige Shop Express
```

5. Sauvegardez et attendez que Render redéploie le service

---

## ✅ Étape 5 : Tester l'envoi d'emails

### Option A : Via le dashboard (recommandé)

1. Allez sur [https://adminprestigeshopexpress.onrender.com](https://adminprestigeshopexpress.onrender.com)
2. Ouvrez **Messages** → **Messagerie Avancée**
3. Sélectionnez des utilisateurs
4. Écrivez un message de test
5. Cliquez sur **Envoyer**
6. Vérifiez votre boîte mail

### Option B : Via cURL (test API direct)

```bash
curl -X POST https://prestige-shop-backend.onrender.com/api/users/send-message \
  -H "Content-Type: application/json" \
  -d '{
    "subject": "Test SendGrid",
    "email_message": "Ceci est un message de test de Prestige Shop Express!",
    "users": [
      {
        "id": 1,
        "prenom": "Jean",
        "nom": "Dupont",
        "email": "votre_email@gmail.com",
        "numero": "0123456789"
      }
    ]
  }'
```

### Option C : Via le script Python

Depuis le terminal du projet :

```bash
python test_sendgrid.py
```

---

## 📊 Monitorer les emails SendGrid

1. Connectez-vous à [https://app.sendgrid.com/](https://app.sendgrid.com/)
2. Allez dans **Email API** → **Stats**
3. Vous verrez :
   - 📧 Nombre d'emails envoyés
   - ✅ Taux de livraison
   - ❌ Bounces/erreurs
   - 📈 Graphiques de performance

---

## 🐛 Dépannage

### ❌ "Clé API SendGrid non configurée"

**Solution :**
- Vérifiez que `SENDGRID_API_KEY` est défini dans Render
- Assurez-vous que la clé est copiée correctement (sans espaces)
- Redéployez le service après avoir ajouté la variable

### ❌ "Email non reçu"

**Vérifiez :**
1. La boîte spam (vérifiez les filtres)
2. L'adresse email est correcte dans la base de données
3. Les logs Render pour les erreurs d'envoi
4. L'email de "From" est vérifié dans SendGrid

### ❌ Erreur 429 (Too Many Requests)

**Cause :** Vous avez dépassé les 100 emails/jour gratuits
**Solution :**
- Attendez jusqu'au lendemain
- Ou upgradez le plan SendGrid (payant, 14-30€/mois pour plus d'emails)

### ❌ Erreur 400 (Bad Request)

**Vérifiez :**
- L'adresse email est valide
- Le message n'est pas vide
- Le format JSON est correct

---

## 📝 Limites du plan gratuit SendGrid

| Limite | Gratuit | Pro |
|--------|---------|-----|
| Emails/jour | 100 | 100,000+ |
| API Calls | Illimitées | Illimitées |
| Email Marketing | ❌ | ✅ |
| Analytics avancée | ❌ | ✅ |
| Support | Communauté | Email 24/7 |
| Prix | 0€ | 19€+ |

---

## 🚀 Prochaines étapes recommandées

1. ✅ **Tester l'envoi** avec quelques emails de test
2. ✅ **Monitorer les résultats** dans SendGrid Dashboard
3. ✅ **Ajouter du logging** pour tracker les envois échoués
4. ✅ **Implémenter les webhooks** SendGrid pour marquer les emails comme "livré"
5. ✅ **Créer des templates** HTML personnalisés dans SendGrid

---

## 📞 Besoin d'aide ?

- Documentation SendGrid : https://docs.sendgrid.com/
- Support SendGrid : https://support.sendgrid.com/
- Forum Communauté : https://github.com/sendgrid/sendgrid-python
