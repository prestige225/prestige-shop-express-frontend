# Prestige Shop Express

Boutique en ligne développée avec HTML, CSS, JavaScript et Flask.

## Structure du projet

- `index.html` - Page principale avec catalogue de produits
- `welcome.html` - Page de bienvenue pour les nouveaux visiteurs
- `login.html` - Page de connexion
- `register.html` - Page d'inscription
- `app.py` - Serveur Flask pour le frontend
- `backend_render/` - Backend Flask avec API
- `css/` - Fichiers de style
- `js/` - Scripts JavaScript
- `images/` - Images du site

## Déploiement sur Render

Le projet est configuré pour être déployé comme une application statique sur Render.

### Frontend
- Type: Static Site
- Build Command: `echo "Building static site"`
- Start Command: `echo "Serving static site"`

### Backend
- Type: Web Service
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn server_fixed:app`

## Fonctionnalités

- Catalogue de produits avec filtres par catégorie
- Panier d'achat avec persistance locale
- Système de favoris
- Authentification utilisateur (inscription/connexion)
- Intégration Google OAuth
- Chatbot d'assistance
- Administration des produits et commandes

## Redirections

La logique de redirection fonctionne comme suit :
1. Les nouveaux visiteurs sont redirigés vers `welcome.html`
2. Les utilisateurs ayant déjà visité le site vont directement sur `index.html`
3. Les utilisateurs connectés sont redirigés vers la page des produits

## Problèmes connus

Si vous rencontrez des problèmes de redirection sur Render :
1. Vérifiez que le fichier `static.json` est présent
2. Assurez-vous que la configuration Render est définie sur "static" et non "python"
3. Redéployez l'application après chaque modification de configuration