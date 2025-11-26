# Configuration de l'authentification Google OAuth

## Étapes à suivre pour configurer l'authentification Google :

### 1. Créer un projet Google Cloud
1. Allez sur [Google Cloud Console](https://console.cloud.google.com/)
2. Créez un nouveau projet ou sélectionnez un projet existant
3. Activez l'API Google+ si ce n'est pas déjà fait

### 2. Configurer les identifiants OAuth
1. Dans le menu de navigation, allez dans "APIs & Services" > "Credentials"
2. Cliquez sur "Create Credentials" > "OAuth client ID"
3. Sélectionnez "Web application" comme type d'application
4. Donnez un nom à votre application (ex: "Prestige Shop Express")
5. Dans "Authorized JavaScript origins", ajoutez :
   - `http://localhost:5000`
   - `http://localhost:3000` (si vous utilisez un autre port)
6. Dans "Authorized redirect URIs", ajoutez :
   - `http://localhost:5000/api/auth/google/callback`
7. Cliquez sur "Create"

### 3. Mettre à jour les identifiants dans le code
1. Copiez le "Client ID" et "Client Secret" générés
2. Dans le fichier `server_fixed.py`, remplacez :
   - `YOUR_GOOGLE_CLIENT_ID` par votre Client ID
   - `YOUR_GOOGLE_CLIENT_SECRET` par votre Client Secret

### 4. Mettre à jour le fichier login.html
1. Dans le fichier [login.html](file:///c%3A/Users/RCK%20COMPUTERS/Desktop/prestige%20shop%20express/login.html), remplacez `YOUR_GOOGLE_CLIENT_ID` par votre Client ID Google

### 5. Installer les dépendances
Assurez-vous que PyJWT est installé :
```bash
pip install PyJWT
```

### 6. Variables d'environnement (optionnel)
Vous pouvez également définir les variables d'environnement suivantes :
- `GOOGLE_CLIENT_ID`
- `GOOGLE_CLIENT_SECRET`
- `GOOGLE_REDIRECT_URI`

## Fonctionnement de l'authentification Google

Lorsqu'un utilisateur clique sur le bouton "Continuer avec Google" :
1. Le SDK Google affiche la fenêtre de connexion Google
2. Après authentification, Google renvoie un token JWT
3. Ce token est envoyé à notre serveur via `/api/auth/google/callback/web`
4. Le serveur vérifie le token et crée/met à jour l'utilisateur dans la base de données
5. L'utilisateur est connecté et redirigé vers l'accueil

## Sécurité

- Le token JWT est vérifié côté serveur
- Les utilisateurs Google n'ont pas de mot de passe dans notre système
- Les sessions sont gérées de la même manière que pour les utilisateurs traditionnels