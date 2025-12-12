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

Le projet est configuré comme un service web Python sur Render pour permettre la communication frontend/backend.

### Frontend
- Type: Web Service
- Environment: Python
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

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
- Frontend: Serveur Flask léger qui sert les fichiers statiques
- Backend: API Flask complète avec base de données
- Communication via AJAX/Fetch API

Les deux services communiquent via des appels RESTful, avec une configuration CORS appropriée.

## Mise à jour du 12/12/2025

Retour à une configuration de service web Python pour garantir la communication frontend/backend :
- Suppression de la configuration statique
- Amélioration des routes Flask pour servir correctement les fichiers statiques
- Ajout d'une route catch-all pour gérer les Single Page Application
- Configuration appropriée pour la communication avec le backend

Cette configuration permet :
1. De servir correctement les fichiers HTML/CSS/JS
2. De maintenir la communication avec le backend API
3. De gérer les redirections côté client comme prévu

## Problèmes connus et solutions

### Interface Render qui s'affiche en premier
Ce problème survient lorsque Render ne reconnaît pas correctement l'application comme un service web Python. Pour le résoudre :

1. Assurez-vous que le fichier `render.yaml` est configuré avec `env: python`
2. Vérifiez que le fichier `requirements.txt` existe avec les dépendances nécessaires
3. Redéployez l'application après chaque modification de configuration

### Problèmes d'authentification (401/500)
Ces erreurs peuvent survenir en raison de problèmes de session entre le frontend et le backend :

1. Vérifiez que les configurations CORS et de session sont correctes
2. Assurez-vous que les cookies sont envoyés avec les requêtes (`credentials: 'include'`)
3. Vérifiez que l'URL du backend est correctement configurée dans `api-config.js`