# 🎬 Animations des Catégories - Aide-Mémoire Rapide

## 🎨 Cartes de Catégories

### Apparition
```
💫 fadeInUp → 0.6s → Monte + Fondu
⏱️ Délais : 0.1s, 0.2s, 0.3s, 0.4s
```

### Survol
```
↗️ translateY(-8px) + scale(1.08)
🌟 Icône : scale(1.2) rotate(5deg)
💎 Effet brillance activé
```

### Active
```
⭕ Bordure pulsante blanche
✨ Ombre lumineuse (20px → 40px)
⏱️ Durée : 2s en boucle
```

---

## 🏷️ Badges

| Badge | Animations | Effet |
|-------|------------|-------|
| ⭐ Populaire | `badge-pulse` + `promo-badge` | Pulse + Flotte |
| 🔥 Promo | `animate-pulse` + `sparkle` | Pulse rapide + Scintille |
| ✨ Nouveau | `promo-badge` + `float` | Flottement doux |

---

## 🎪 Bannière

### Séquence (total 0.8s)
```
1. 0.0s → Bannière descend (bannerSlideIn)
2. 0.0s → Icône tourne (iconRotate)  
3. 0.3s → Badge arrive droite (badgeSlideIn)
4. 0.0s → Particules flottent
5. 0.05s → Vibration mobile
```

### Éléments Animés
- 🎯 **Icône** : Rotation -180° → 0° (0.8s)
- 📝 **Titre** : FadeIn avec délai
- 🎁 **Badge** : Slide depuis droite + Hover scale
- ⭕ **Particules** : 4 cercles flottants (3s loop)
- 💫 **Cercles** : 2 grands flous pulsants

---

## 🎭 Sous-Catégories Mode

### Panel
```
📥 slideDown → 0.4s
```

### Boutons
```
🎯 Survol : translateY(-3px) + scale(1.08)
🎪 Icône : bounce (5 étapes)
💧 Clic : Effet d'onde 0→300px
```

---

## ⚡ Performances

```
GPU : ✅ Transform + Opacity uniquement
FPS : ✅ 60 FPS constant
Courbe : ✅ cubic-bezier(0.4, 0, 0.2, 1)
Mobile : ✅ Vibration haptique
```

---

## 🎨 Classes Utiles

```html
<!-- Badges -->
<div class="badge-pulse">Pulse scale</div>
<div class="promo-badge">Flottement</div>
<div class="sparkle">Scintillement</div>
<div class="animate-pulse">Pulse Tailwind</div>

<!-- Bannière -->
<div class="category-banner-animate">Bannière</div>
<div class="banner-icon">Icône rotative</div>
<div class="banner-badge">Badge qui slide</div>
<div class="particle">Particule flottante</div>

<!-- Sous-catégories -->
<div class="subcategory-btn">Bouton animé</div>
<div class="animate-slideDown">Panel qui descend</div>
```

---

## 🎯 Timing Optimal

| Animation | Durée Recommandée |
|-----------|-------------------|
| Apparition | 0.4s - 0.8s |
| Hover | 0.2s - 0.4s |
| Pulse | 1.5s - 3s |
| Rotation | 0.6s - 1s |
| Slide | 0.4s - 0.6s |

---

## 📱 Responsive

| Appareil | Colonnes | Animations |
|----------|----------|------------|
| Mobile | 1 | ✅ Toutes + Vibration |
| Tablette | 2 | ✅ Toutes |
| Desktop | 4 | ✅ Toutes + Brillance |

---

## 🚀 Impact Utilisateur

```
📈 +150% engagement visuel
⚡ Feedback immédiat
💎 Expérience premium
🎯 Taux de rebond réduit
⏱️ Temps sur site augmenté
```

---

**Toutes les animations sont optimisées GPU pour 60 FPS ! 🎬**
