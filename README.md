# Prestige Shop Express

Boutique en ligne développée avec HTML, CSS, JavaScript et Flask.

## Structure du projet

- `index.html` - Page principale avec catalogue de produits
- `welcome.html` - Page de bienvenue pour les nouveaux visiteurs
- `login.html` - Page de connexion
- `register.html` - Page d'inscription
- `app.py` - Serveur Flask pour le frontend (utilisé uniquement pour le déploiement sur Render)
- `backend_render/` - Backend Flask avec API
- `css/` - Fichiers de style
- `js/` - Scripts JavaScript
- `images/` - Images du site

## Déploiement sur Render

Le projet est configuré comme un site statique sur Render pour servir les fichiers HTML/CSS/JS, avec un serveur Flask léger pour le déploiement.

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

## Communication Frontend/Backend

L'application utilise une architecture frontend/backend séparés :
- Frontend: Fichiers statiques servis par Render
- Backend: API Flask complète avec base de données
- Communication via AJAX/Fetch API

Les deux services communiquent via des appels RESTful, avec une configuration CORS appropriée.

## Mise à jour du 12/12/2025

Changement de stratégie pour le déploiement frontend :
- Passage à un déploiement de site statique sur Render
- Création du fichier `static.json` pour configurer le routage
- Conservation de `app.py` pour assurer la compatibilité avec Render
- Configuration appropriée pour la communication avec le backend

Cette configuration permet :
1. De servir correctement les fichiers HTML/CSS/JS sans interface Render
2. De maintenir la communication avec le backend API
3. De gérer les redirections côté client comme prévu

## Problèmes connus et solutions

### Interface Render qui s'affiche en premier
Ce problème survient lorsque Render ne reconnaît pas correctement l'application comme un site statique. Pour le résoudre :

1. Assurez-vous que le fichier `render.yaml` est configuré avec `env: static`
2. Vérifiez que le fichier `static.json` existe avec la configuration appropriée
3. Redéployez l'application après chaque modification de configuration

### Problèmes d'authentification (401/500)
Ces erreurs peuvent survenir en raison de problèmes de session entre le frontend et le backend :

1. Vérifiez que les configurations CORS et de session sont correctes
2. Assurez-vous que les cookies sont envoyés avec les requêtes (`credentials: 'include'`)
3. Vérifiez que l'URL du backend est correctement configurée dans `api-config.js`