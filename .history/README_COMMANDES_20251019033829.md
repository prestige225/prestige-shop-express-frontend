# Gestion des Commandes - Prestige Shop Express

## 📦 Table: commandes

### Structure de la table

```sql
CREATE TABLE commandes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    numero_commande VARCHAR(50) NOT NULL UNIQUE,
    date_commande DATETIME DEFAULT CURRENT_TIMESTAMP,
    statut ENUM('en_attente', 'en_cours', 'livree', 'annulee') DEFAULT 'en_attente',
    montant_total DECIMAL(10,2) NOT NULL,
    adresse_livraison TEXT NOT NULL,
    telephone VARCHAR(20) NOT NULL,
    notes TEXT
);
```

## 🚀 Installation

### 1. Créer la table dans la base de données

Exécutez le fichier SQL:
```bash
mysql -u usblj9n0kraq8uoc -p -h bracv1wswmu4vsqxycku-mysql.services.clever-cloud.com bracv1wswmu4vsqxycku < table_commandes.sql
```

Ou copiez-collez le contenu de `table_commandes.sql` dans votre client MySQL.

### 2. Démarrer le serveur Flask

```bash
python server_fixed.py
```

Le serveur démarrera sur `http://localhost:5000`

## 📡 Routes API Disponibles

### 1. Récupérer toutes les commandes (Admin)
```http
GET /api/commandes
```

**Réponse:**
```json
{
    "success": true,
    "data": [
        {
            "id": 1,
            "user_id": 1,
            "numero_commande": "CMD-20241019120000-123",
            "date_commande": "2024-10-19T12:00:00",
            "statut": "en_attente",
            "montant_total": 45000.00,
            "adresse_livraison": "Cocody Angré...",
            "telephone": "0758415088",
            "notes": "Livraison avant 18h",
            "nom": "Doe",
            "prenom": "John",
            "email": "john@example.com"
        }
    ]
}
```

### 2. Récupérer les commandes d'un utilisateur
```http
GET /api/commandes/user/{user_id}
```

**Exemple:**
```http
GET /api/commandes/user/1
```

### 3. Récupérer une commande spécifique
```http
GET /api/commandes/{commande_id}
```

**Exemple:**
```http
GET /api/commandes/5
```

### 4. Créer une nouvelle commande
```http
POST /api/commandes
Content-Type: application/json

{
    "user_id": 1,
    "montant_total": 45000.00,
    "adresse_livraison": "Cocody Angré 7ème Tranche",
    "telephone": "0758415088",
    "notes": "Livraison avant 18h svp"
}
```

**Réponse:**
```json
{
    "success": true,
    "message": "Commande créée avec succès",
    "commande_id": 10,
    "numero_commande": "CMD-20241019153045-789",
    "data": {
        "id": 10,
        "numero_commande": "CMD-20241019153045-789",
        "statut": "en_attente",
        "montant_total": 45000.00
    }
}
```

### 5. Mettre à jour une commande
```http
PUT /api/commandes/{commande_id}
Content-Type: application/json

{
    "statut": "en_cours"
}
```

**Champs modifiables:**
- `statut`: 'en_attente', 'en_cours', 'livree', 'annulee'
- `adresse_livraison`
- `telephone`
- `notes`

### 6. Supprimer une commande
```http
DELETE /api/commandes/{commande_id}
```

## 🖥️ Pages Web Créées

### 1. admin_commandes.html
**URL:** `http://localhost:5000/admin_commandes.html`

**Fonctionnalités:**
- ✅ Tableau de bord avec statistiques des commandes
- ✅ Liste complète de toutes les commandes
- ✅ Filtrage par statut
- ✅ Recherche par numéro de commande ou nom de client
- ✅ Mise à jour du statut des commandes
- ✅ Affichage des détails de chaque commande
- ✅ Suppression de commandes
- ✅ Actualisation automatique toutes les 30 secondes

**Accès:**
```
http://localhost:5000/admin_commandes.html
```

### 2. mes_commandes.html
**URL:** `http://localhost:5000/mes_commandes.html`

**Fonctionnalités:**
- ✅ Affichage des commandes de l'utilisateur connecté
- ✅ Statistiques personnelles (total, en attente, en cours, livrées)
- ✅ Suivi de l'état de chaque commande avec timeline visuelle
- ✅ Détails complets de chaque commande
- ✅ Possibilité d'annuler une commande en attente
- ✅ Contact direct via WhatsApp pour support
- ✅ Filtrage par statut

**Accès:**
```
http://localhost:5000/mes_commandes.html
```

### 3. admin.html (Mise à jour)
Ajout d'un bouton "Commandes" dans le header pour accéder à la gestion des commandes.

## 💻 Utilisation dans le Code Frontend

### Créer une commande depuis le panier

```javascript
async function passerCommande() {
    const userData = JSON.parse(localStorage.getItem('userData'));
    
    const commandeData = {
        user_id: userData.id,
        montant_total: calculateTotal(),
        adresse_livraison: document.getElementById('adresse').value,
        telephone: document.getElementById('telephone').value,
        notes: document.getElementById('notes').value
    };
    
    try {
        const response = await fetch('http://localhost:5000/api/commandes', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(commandeData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert(`Commande créée avec succès! Numéro: ${data.numero_commande}`);
            // Vider le panier
            localStorage.removeItem('cart');
            // Rediriger vers mes commandes
            window.location.href = 'mes_commandes.html';
        }
    } catch (error) {
        console.error('Erreur:', error);
        alert('Erreur lors de la création de la commande');
    }
}
```

### Récupérer les commandes d'un utilisateur

```javascript
async function chargerMesCommandes() {
    const userData = JSON.parse(localStorage.getItem('userData'));
    
    try {
        const response = await fetch(`http://localhost:5000/api/commandes/user/${userData.id}`);
        const data = await response.json();
        
        if (data.success) {
            afficherCommandes(data.data);
        }
    } catch (error) {
        console.error('Erreur:', error);
    }
}
```

## 🎨 Statuts des Commandes

| Statut | Description | Couleur | Icône |
|--------|-------------|---------|-------|
| `en_attente` | Commande reçue, en attente de traitement | Jaune | 🕐 |
| `en_cours` | Commande en cours de préparation/livraison | Orange | 🚚 |
| `livree` | Commande livrée au client | Vert | ✅ |
| `annulee` | Commande annulée | Rouge | ❌ |

## 🔐 Sécurité

Les routes API sont protégées et fonctionnent avec:
- Validation des données côté serveur
- Gestion des erreurs appropriée
- Support CORS pour les requêtes cross-origin
- Transactions sécurisées avec la base de données

## 📊 Fonctionnalités Clés

### Pour l'Administration
1. **Dashboard des commandes** avec statistiques en temps réel
2. **Gestion complète** du cycle de vie des commandes
3. **Recherche et filtrage** avancés
4. **Mise à jour rapide** des statuts
5. **Accès aux informations clients**

### Pour les Utilisateurs
1. **Historique complet** des commandes
2. **Suivi en temps réel** avec timeline visuelle
3. **Annulation** des commandes en attente
4. **Contact direct** via WhatsApp
5. **Interface responsive** pour mobile et desktop

## 🔄 Workflow Typique

1. **Client crée une commande** depuis le panier
   - Statut initial: `en_attente`
   - Numéro unique généré automatiquement

2. **Admin traite la commande**
   - Vérifie les détails
   - Change le statut à `en_cours`

3. **Livraison**
   - Commande préparée et expédiée
   - Statut reste `en_cours`

4. **Confirmation de livraison**
   - Admin marque comme `livree`
   - Client peut voir le statut final

## 🛠️ Personnalisation

### Modifier les statuts disponibles

Dans `server_fixed.py`:
```python
statut ENUM('en_attente','en_cours','livree','annulee','autre_statut')
```

### Ajouter des champs à la table

```sql
ALTER TABLE commandes ADD COLUMN mode_paiement VARCHAR(50);
ALTER TABLE commandes ADD COLUMN frais_livraison DECIMAL(10,2);
```

## 📱 Responsive Design

Toutes les pages sont optimisées pour:
- 📱 Smartphones
- 💻 Tablettes
- 🖥️ Desktop

## 🌐 Déploiement

Les pages fonctionnent avec le serveur Flask:
```bash
python server_fixed.py
```

Accès aux pages:
- Admin Commandes: `http://localhost:5000/admin_commandes.html`
- Mes Commandes: `http://localhost:5000/mes_commandes.html`
- Admin Utilisateurs: `http://localhost:5000/admin.html`
- Boutique: `http://localhost:5000/index.html`

## 📞 Support

Pour toute question concernant l'implémentation:
- WhatsApp: +225 07 58 41 50 88
- Email: support@prestige-shop-express.com

## ✅ Checklist de Déploiement

- [x] Table `commandes` créée dans la base de données
- [x] Routes API testées et fonctionnelles
- [x] Page admin des commandes opérationnelle
- [x] Page utilisateur des commandes opérationnelle
- [x] Navigation entre les pages configurée
- [x] Design responsive vérifié
- [x] Gestion des erreurs implémentée
- [x] Documentation complète

---

**Développé avec ❤️ pour Prestige Shop Express**
