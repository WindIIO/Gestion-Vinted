# ⚡ DÉMARRAGE RAPIDE - 3 ÉTAPES

## 🚀 Lancer l'Application

### Option A: Clic simple (Windows)

**Double-cliquez** le fichier: `launch.bat`

### Option B: En ligne de commande

```bash
cd "c:\Users\ribel\Desktop\LeReacteur-Preparation\Portefolio\Gestion Vinted"
python vinted_app/main.py
```

### Option C: Via VS Code

1. Ouvrir le dossier du projet
2. Ouvrir le Terminal (Ctrl + `)
3. Taper: `python vinted_app/main.py`

---

## 📋 Première Utilisation

### 1. Consulter le Dashboard 📊

- L'application s'ouvre sur le dashboard
- Vous voyez 5 produits de test
- Bénéfice total: 22€

### 2. Voir tous les Produits 📦

- Cliquez **"📦 Produits"** dans la sidebar
- Vous voyez une liste avec filtres
- Cherchez par nom

### 3. Ajouter votre Produit ➕

- Cliquez **"➕ Ajouter Produit"**
- Remplissez le formulaire
- Cliquez **"✓ Ajouter Produit"**

---

## 🎮 Guide d'Utilisation Simple

### Dashboard

- Voir tous les chiffres importants
- Total investi, Total gagné, Bénéfice total, Marge %
- Statistiques par catégorie

### Produits

- **Filtrer**: En Stock, En Vente, Vendus, Tous
- **Chercher**: Recherche par nom
- **✓ Vendre**: Marquer comme vendu
- **✕**: Supprimer un produit

### Ajouter

1. **Nom**: Nom du produit
2. **Catégorie**: Sélectionner dans la liste
3. **Plateforme**: Vinted, Leboncoin, etc.
4. **État**: Neuf, Très bon, etc.
5. **Prix achat**: Montant payé
6. **Prix vente**: Montant de vente prévu
7. **Frais**: Commission (ex: 3,5€ pour Vinted)
8. **Quantité**: Nombre d'articles
9. **📊 Calculer**: Voir le bénéfice estimé
10. **✓ Ajouter**: Enregistrer

---

## 💡 Données Pré-chargées

L'app inclut 5 produits de test:

| Produit           | Prix Achat | Prix Vente | Statut   |
| ----------------- | ---------- | ---------- | -------- |
| Jean Levi's 501   | 15€        | 28€        | En Vente |
| Nike Air Force 1  | 35€        | 65€        | Vendu ✓  |
| Sac Louis Vuitton | 120€       | 250€       | En Stock |
| T-shirt Vintage   | 8€         | 22€        | En Stock |
| PS5 Manette       | 45€        | 85€        | En Stock |

**Supprimez-les** et **ajoutez vos propres produits**!

---

## 🌈 Couleurs

- 🟢 **Vert**: Produit vendu
- 🟠 **Orange**: Produit en vente
- ⚫ **Gris**: Produit en stock

---

## 🆘 Problèmes?

### L'app ne démarre pas?

```bash
pip install customtkinter
python vinted_app/main.py
```

### La DB est corrompue?

1. Fermez l'app
2. Trouvez: `vinted_app/data/vinted.db`
3. Supprimez ce fichier
4. Relancez l'app (tout sera régénéré)

### J'ai des questions?

- Lire: `README.md`
- Guide complet: `GUIDE_LANCEMENT.md`

---

## 📚 Fichiers Importants

```
🎯 launch.bat           ← Clicker pour démarrer
📖 README.md            ← Documentation complète
🚀 GUIDE_LANCEMENT.md   ← Guide détaillé
👨‍💻 DEV_GUIDE.md        ← Pour développeurs
📝 RÉSUMÉ.md            ← Résumé du projet
📂 vinted_app/          ← Code de l'app
```

---

## ✨ Fonctionnalités Clés

✅ Dashboard avec KPIs
✅ Gestion produits (CRUD)
✅ Filtres et recherche
✅ Calcul profit/marge automatique
✅ ROI et statistiques
✅ Interface intuitive
✅ Données persistantes (SQLite)
✅ Prêt pour production

---

## 🎉 C'est Tout!

Votre application est prête. Commencez à gérer vos produits Vinted maintenant!

**Lancez**: `python vinted_app/main.py`

Bon trading! 📈💰
