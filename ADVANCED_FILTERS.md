# 🆕 Filtres Avancés - Guide Utilisateur

## 📋 Nouveaux Filtres Disponibles

Le système de messagerie supporte maintenant des filtres avancés basés sur le **profil utilisateur** :

### 1️⃣ Statut Profil
Filtre par la catégorie professionnelle/éducative :
- **Élève** - Utilisateurs en scolarité primaire/secondaire
- **Étudiant** - Utilisateurs en études supérieures
- **Parent** - Parents d'enfants
- **Professeur** - Enseignants et formateurs
- **Travailleur** - Actifs professionnels
- **Autre** - Autres catégories

### 2️⃣ Sexe
Filtre par genre :
- **Homme**
- **Femme**
- **Tous** (par défaut)

### 3️⃣ Âge
Filtre par tranche d'âge avec deux champs :
- **Âge minimum** - Âge minimum inclus
- **Âge maximum** - Âge maximum inclus

**Exemples** :
- Min: 18, Max: 25 → Utilisateurs entre 18 et 25 ans
- Min: 30 → Utilisateurs de 30 ans et plus
- Max: 50 → Utilisateurs jusqu'à 50 ans

### 4️⃣ Adresse
Filtre par localisation :
- Cherche dans les adresses, villes, régions
- Recherche **partiellement** (ex: "Paris" trouve toutes les adresses avec Paris)

**Exemples** :
- "Paris" → Tous les Parisiens
- "75" → Code postal Paris
- "Île-de-France" → Région

### 5️⃣ Centres d'Intérêt
Filtre par intérêts et hobbies :
- Recherche **partiellement** dans les centres d'intérêt
- Peut contenir plusieurs mots-clés

**Exemples** :
- "Sport" → Tous les sportifs
- "Lecture" → Amateurs de lecture
- "Tech" → Passionnés de technologie
- "Art" → Amateurs d'art

---

## 🎯 Comment Utiliser les Filtres

### Étape 1 : Définir les Filtres
1. Allez sur l'interface de messagerie : `admin/messages.html`
2. Remplissez les filtres souhaités à gauche
3. Les filtres peuvent être combinés pour une recherche plus précise

### Étape 2 : Charger les Utilisateurs
1. Cliquez sur le bouton **"Charger Utilisateurs"**
2. Le système charge UNIQUEMENT les utilisateurs correspondant aux filtres
3. La liste s'affiche à gauche avec les informations du profil

### Étape 3 : Affiner les Résultats
1. Cochez les utilisateurs manuellement
2. Ou utilisez **"Sélectionner Tous"** pour tous les résultats filtrés
3. La barre de recherche rapide affine encore plus

### Étape 4 : Envoyer le Message
1. Composez votre message à droite
2. Confirmez et envoyez

---

## 💡 Exemples de Campagnes Ciblées

### 📚 Campagne Étudiants
```
Statut Profil : Étudiant
Âge Min : 18
Âge Max : 25
→ Cible les étudiants âgés de 18 à 25 ans
```

### 👨‍💼 Campagne Professionnels
```
Statut Profil : Travailleur
Âge Min : 25
→ Cible les travailleurs de 25 ans et plus
```

### 🎓 Campagne Professeurs
```
Statut Profil : Professeur
→ Cible uniquement les enseignants
```

### 📍 Campagne Régionale
```
Adresse : Île-de-France
→ Cible les utilisateurs en Île-de-France
```

### 🎨 Campagne Hobbyistes
```
Centres d'Intérêt : Art
Sexe : Femme
→ Cible les femmes intéressées par l'art
```

### 🏃 Campagne Actifs Sportifs
```
Statut Profil : Travailleur
Centres d'Intérêt : Sport
Âge Min : 20
Âge Max : 50
→ Cible les travailleurs sportifs entre 20 et 50 ans
```

---

## 🔍 Comportement des Filtres

### Combinaison des Filtres
Tous les filtres actifs sont combinés avec **ET** (AND logic) :
- Statut Profil = "Étudiant" **ET**
- Sexe = "Femme" **ET**
- Âge >= 20 **ET**
- Adresse contient "Paris"

### Filtres Vides
Les filtres vides sont **ignorés** :
- Laisser un champ vide = inclure toutes les valeurs pour ce champ
- Exemple : Laisser Sexe vide = pas de filtrage par sexe

### Recherche Partielle
Les champs texte font une recherche partielle (LIKE) :
- "Paris" trouve : Paris, Île-de-France, Centre de Paris, etc.
- Case-insensitive (majuscules/minuscules ignorées)

### Recherche Numérique
Les champs d'âge acceptent uniquement les nombres :
- Vide = pas de limitation
- "0" à "150" = plage valide

---

## 📊 Affichage des Utilisateurs Filtrés

Chaque utilisateur affiche :
- ✔️ **Case de sélection** - Cochez pour inclure
- 👤 **Nom et Prénom**
- 📧 **Email**
- 🏷️ **Statut Profil** (badge bleu) - Ex: "Étudiant"
- 👥 **Sexe** (badge violet) - Ex: "Femme"
- 🎂 **Âge** (badge orange) - Ex: "22ans"

---

## ⚙️ Spécifications Techniques

### Endpoint Backend
```
POST /api/users/filter
```

### Paramètres
```json
{
  "statut": "Étudiant",          // Statut profil
  "sexe": "Femme",               // Homme ou Femme
  "age_min": 20,                 // Âge minimum
  "age_max": 30,                 // Âge maximum
  "adresse": "Paris",            // Cherche partiellement
  "centre_interet": "Sport"      // Cherche partiellement
}
```

### Réponse
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
      "statut": "actif",
      "statut_profil": "Étudiant",
      "sexe": "Homme",
      "age": 22,
      "adresse": "75001 Paris",
      "centre_interet": "Sport, Lecture"
    }
  ]
}
```

---

## 🚀 Cas d'Usage Avancés

### Segmentation Multi-Critères
Créez des segments sophistiqués :
1. Femmes de 25-35 ans, travailleuses, intéressées par l'art
2. Hommes de 18-25 ans, étudiants, intéressés par la tech
3. Parents d'Île-de-France, intéressés par l'éducation

### Campagnes Saisonnières
Ajustez les critères selon la saison :
- **Été** : Ciblez les vacanciers (centres d'intérêt: voyage)
- **Noël** : Ciblez les parents (statut: parent)
- **Rentrée** : Ciblez les étudiants (statut: étudiant)

### Relance Client Dormant
1. Filtrez par date de dernière connexion (si disponible)
2. Combinez avec des intérêts spécifiques
3. Envoyez une offre personnalisée

### Newsletter Thématique
1. Filtre par centre d'intérêt
2. Envoyez un contenu adapté à chaque groupe

---

## ✅ Checklist Avant Envoi

Avant de valider un envoi en masse :

- [ ] Au moins un filtre défini ou tous les utilisateurs voulus?
- [ ] Résultats affichés correspondent-ils à l'attente?
- [ ] Nombre d'utilisateurs sélectionnés correct?
- [ ] Le message est personnalisé ({{prenom}}, etc.)?
- [ ] Confirmation cochée?

---

**Besoin d'aide ?** Consultez [MESSAGING_SYSTEM.md](MESSAGING_SYSTEM.md) pour la documentation complète.

---

*Version: 1.1 - Filtres Avancés*
*Date: 15 décembre 2025*
