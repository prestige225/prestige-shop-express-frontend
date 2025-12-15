# 📧 Système de Gestion des Messages - Documentation Complète

## 🎯 Vue d'ensemble

Nouveau système complet et intégré pour envoyer des messages personnalisés à vos utilisateurs, directement depuis la base de données.

---

## 📁 Fichiers Impliqués

### Frontend
- **`admin/messages.html`** - Interface principale (NOUVEAU)
- **`admin/admin.html`** - Tableau de bord admin (modifié - lien mis à jour)
- **`admin/api-config.js`** - Configuration API (inchangé)

### Backend  
- **`backend_render/server_fixed.py`** - API Flask (modifié - nouvel endpoint ajouté)
- **`backend_render/message_sender.py`** - Moteur d'envoi (inchangé mais utilisé)

---

## ⚙️ Fonctionnalités Principales

### 1️⃣ Chargement des Utilisateurs
- Cliquez sur **"Charger Utilisateurs"** pour récupérer tous les utilisateurs actifs de la base de données
- Les utilisateurs s'affichent avec checkboxes à gauche

### 2️⃣ Filtrage & Recherche
- **Filtre par Statut** : Voir tous / Actifs / Inactifs
- **Recherche** : Par nom prénom ou email (en temps réel)

### 3️⃣ Sélection Manuelle
- Cochez les utilisateurs à qui vous voulez envoyer le message
- Utilisez **"Sélectionner Tous"** ou **"Désélectionner Tous"** pour actions rapides
- Le compteur en haut indique le nombre d'utilisateurs sélectionnés

### 4️⃣ Composition du Message
- **Objet Email** (obligatoire) : Titre qui apparaît dans les boîtes de réception
- **Contenu Email** (obligatoire) : Corps du message avec support de variables
- **Message WhatsApp** (optionnel) : Message pour les utilisateurs ayant un numéro

### 5️⃣ Variables de Personnalisation
Les messages sont automatiquement personnalisés pour chaque utilisateur :
- `{{prenom}}` → Remplacé par le prénom
- `{{nom}}` → Remplacé par le nom  
- `{{email}}` → Remplacé par l'email

**Exemple :**
```
Bonjour {{prenom}} {{nom}},

Bienvenue chez Prestige Shop Express !
Nous sommes heureux de vous compter parmi nos clients.

Visitez notre site : https://prestige-shop-express.onrender.com/

À bientôt !
```

Sera envoyé comme :
- À Ahmed Dupont : "Bonjour Ahmed Dupont, ..."
- À Fatima Martin : "Bonjour Fatima Martin, ..."

### 6️⃣ Envoi des Messages
1. Cochez la case **"Je confirme l'envoi à X utilisateur(s)"**
2. Cliquez sur **"Envoyer les Messages"**
3. Attendez la confirmation ✅
4. Le système affiche le nombre d'emails et de WhatsApp envoyés

---

## 🔄 Flux Complet d'Utilisation

```
1. Tableau de bord admin → Cliquer sur "Messages"
   ↓
2. Interface chargée → Cliquer sur "Charger Utilisateurs"
   ↓
3. Utilisateurs affichés → Sélectionner ceux qui veulent recevoir le message
   ↓
4. Remplir l'objet et le contenu (avec variables si souhaité)
   ↓
5. Cocher la confirmation et envoyer
   ↓
6. Succès ! ✅ Affichage du nombre de messages envoyés
```

---

## 🛠️ API Endpoints

### Récupérer les Utilisateurs Actifs
```http
GET /api/users/active
```

**Réponse :**
```json
{
  "success": true,
  "users": [
    {
      "id": 1,
      "prenom": "Ahmed",
      "nom": "Dupont",
      "email": "ahmed@example.com",
      "numero": "0612345678",
      "statut": "actif"
    },
    ...
  ]
}
```

### Envoyer des Messages en Masse
```http
POST /api/messages/send-bulk
Content-Type: application/json

{
  "subject": "Bienvenue {{prenom}} !",
  "email_message": "Bonjour {{prenom}} {{nom}}, ...",
  "whatsapp_message": "Bonjour {{prenom}}, ...",
  "users": [
    {
      "id": 1,
      "prenom": "Ahmed",
      "nom": "Dupont",
      "email": "ahmed@example.com",
      "numero": "0612345678"
    }
  ]
}
```

**Réponse :**
```json
{
  "success": true,
  "emailsSent": 1,
  "whatsappSent": 1,
  "message": "Messages envoyés avec succès à 1 utilisateurs"
}
```

---

## 📊 Structure de la Base de Données (Table `users`)

| Colonne | Type | Usage |
|---------|------|-------|
| `id` | INT | Identifiant unique |
| `prenom` | VARCHAR | Variable {{prenom}} |
| `nom` | VARCHAR | Variable {{nom}} |
| `email` | VARCHAR | Envoi des emails |
| `numero` | VARCHAR | Envoi WhatsApp |
| `statut` | VARCHAR | Filtrage (actif/inactif) |
| `session_active` | INT | Statut connexion |
| `date_inscription` | DATETIME | Date d'arrivée |
| `derniere_connexion` | DATETIME | Dernière visite |

---

## 🎨 Interface Utilisateur

### Panneau Gauche (Sélection)
- Bouton "Charger Utilisateurs"
- Filtre par statut (dropdown)
- Recherche en temps réel
- Boutons "Sélectionner Tous" / "Désélectionner Tous"
- **Compteur** affichant le nombre d'utilisateurs sélectionnés
- **Liste des utilisateurs** avec checkboxes et badges de statut

### Panneau Droit (Composition)
- Champ "Objet de l'Email" 
- Zone texte "Contenu de l'Email" (10 lignes)
- Zone texte "Message WhatsApp" (3 lignes, optionnel)
- Cases à cocher pour confirmation
- Boutons "Envoyer" et "Réinitialiser"
- **Section Résultats** (cachée par défaut)

---

## ✅ Checklist d'Utilisation

Avant d'envoyer un message :

- [ ] Page chargée et API accessible
- [ ] Utilisateurs chargés avec succès  
- [ ] Au moins un utilisateur sélectionné
- [ ] Objet de l'email rempli
- [ ] Contenu de l'email rempli
- [ ] Variables de personnalisation ajoutées (optionnel mais recommandé)
- [ ] Confirmation cochée
- [ ] Prêt à envoyer !

---

## 🚀 Points Clés

✅ **Sélection manuelle** - Vous choisissez exactement qui reçoit le message
✅ **Personnalisation automatique** - {{prenom}}, {{nom}}, {{email}} remplacés
✅ **Filtrage rapide** - Par statut ou recherche
✅ **Interface intuitive** - Deux panneaux : sélection + composition
✅ **Confirmation requise** - Évite les envois accidentels
✅ **Feedback immédiat** - Affichage des résultats

---

## 🔗 Ressources

- **URL Admin** : `https://adminprestigeshopexpress.onrender.com/admin/admin.html`
- **Bouton Messages** : Dans le tableau de bord admin
- **Page Messages** : `/admin/messages.html`

---

## ⚠️ Limitations & Notes

- Les messages sont **personnalisés au moment de l'envoi** pour chaque utilisateur
- Seuls les utilisateurs avec `statut = 'actif'` sont affichés
- Les emails sont envoyés uniquement si l'utilisateur a une adresse email
- Les WhatsApp sont envoyés uniquement si l'utilisateur a un numéro de téléphone
- La confirmation est obligatoire pour éviter les envois accidentels

---

**Dernière mise à jour** : 2025-01-01
**Version** : 1.0 - Complet et Prêt à l'Emploi ✅
