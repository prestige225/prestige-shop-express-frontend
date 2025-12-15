# 📧 Configuration SendGrid sur Render

## Étape 1 : Créer un compte SendGrid gratuit

1. Allez sur [sendgrid.com](https://sendgrid.com)
2. Cliquez sur **"Start Free"**
3. Remplissez le formulaire d'inscription
4. Vérifiez votre email
5. Connectez-vous à votre dashboard SendGrid

## Étape 2 : Créer une clé API

1. Dans le dashboard SendGrid, allez à **Settings → API Keys**
2. Cliquez sur **"Create API Key"**
3. Nommez-la : `PrestigeShopExpress`
4. Sélectionnez les permissions : **Mail Send**
5. Cliquez sur **Create & Copy**
6. **Sauvegardez cette clé** (vous ne pourrez pas la voir à nouveau)

## Étape 3 : Vérifier votre adresse email

1. Dans SendGrid, allez à **Settings → Sender Authentication**
2. Cliquez sur **"Verify a Single Sender"**
3. Entrez votre email : `contact@prestigeshopexpress.com` (ou l'email de votre entreprise)
4. Remplissez les détails de votre entreprise
5. Cliquez sur le lien de vérification dans votre email

## Étape 4 : Configurer les variables d'environnement sur Render

1. Allez sur [render.com](https://render.com)
2. Sélectionnez votre service backend : **prestige-shop-backend**
3. Allez à **Environment** (ou Settings)
4. Ajoutez ces variables :

```
SENDGRID_API_KEY = votre_clé_api_sendgrid
SENDGRID_FROM_EMAIL = contact@prestigeshopexpress.com
SENDGRID_FROM_NAME = Prestige Shop Express
```

5. Cliquez sur **Save Changes**
6. Le service va redéployer automatiquement

## Étape 5 : Tester l'envoi d'email

Une fois configuré, les emails seront envoyés via :
- ✅ Endpoint API : `POST /api/users/send-message`
- ✅ Interface admin : https://adminprestigeshopexpress.onrender.com/admin_messages.html

## Limites SendGrid Gratuit

- ✅ **100 emails/jour** (suffisant pour une petite entreprise)
- ✅ Support basique inclus
- ✅ Authentification 2FA disponible
- ⚠️ Pas de webhooks avancés

## Troubleshooting

### Emails non reçus ?

1. ✅ Vérifiez que la clé API est configurée sur Render
2. ✅ Vérifiez que l'email de départ est vérifié dans SendGrid
3. ✅ Vérifiez les logs Render : `Render → Logs`
4. ✅ Vérifiez le dossier spam des destinataires

### Erreur "Unauthorized" ?

- La clé API n'est pas valide ou n'est pas dans la bonne variable d'environnement
- Redéployez le service après avoir changé les variables

### Comment voir les statistiques ?

Dans SendGrid Dashboard :
- **Stats** : Voir les emails envoyés, ouverts, cliqués
- **Bounces** : Voir les adresses invalides
- **Complaints** : Voir les signalements de spam
