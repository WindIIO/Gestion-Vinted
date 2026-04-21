# Vinted Stock Manager 📊

Application complète de gestion de stock pour achat/revente Vinted avec interface graphique moderne.

## 🚀 Installation

### Prérequis

- Python 3.8+
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou extraire le projet**

```bash
cd vinted_app
```

2. **Créer un environnement virtuel (recommandé)**

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

## 🏃 Lancer l'application

Une fois dans le dossier du projet et l'environnement virtuel activé :

```bash
python main.py
```

## 📋 Fonctionnalités

### 1. **Dashboard 📊**

- Vue d'ensemble de tous les KPIs
- Total investi, total gagné, bénéfice total
- Statistiques par catégorie et plateforme
- Analyse avancée (ROI, bénéfice moyen, etc.)

### 2. **Gestion des Produits 📦**

- Ajouter des produits avec tous les détails
- Liste complète avec filtrage (Stock, En Vente, Vendu)
- Recherche par nom/catégorie/plateforme
- Modifier le statut des produits
- Supprimer les produits

### 3. **Calculs Financiers 💰**

- Calcul automatique du bénéfice (vente - achat - frais)
- Marge de profit en pourcentage
- ROI (Return on Investment)
- Statistiques par catégorie

### 4. **Interface Intuitive 🎨**

- Design moderne avec CustomTkinter
- Sidebar de navigation
- Codes couleur (vert = vendu, orange = en vente, gris = stock)
- Responsive et facile à utiliser

## 📁 Structure du Projet

```
vinted_app/
├── main.py                  # Point d'entrée
├── config.py               # Configuration globale
├── database/
│   ├── db.py              # Gestion SQLite
│   └── models.py          # Modèles de données
├── services/
│   ├── product_service.py # Gestion des produits
│   ├── finance_service.py # Calculs financiers
│   └── stats_service.py   # Statistiques
├── ui/
│   ├── main_window.py     # Fenêtre principale
│   ├── dashboard.py       # Dashboard
│   ├── product_list.py    # Liste des produits
│   └── add_product.py     # Formulaire d'ajout
├── utils/
│   └── helpers.py         # Fonctions utilitaires
├── assets/                # Images et ressources
└── data/                  # Base de données (créée automatiquement)
```

## 🗄️ Base de Données

La base de données SQLite est créée automatiquement dans `data/vinted.db`

Champs de la table **products** :

- id : Identifiant unique
- name : Nom du produit
- category : Catégorie
- platform : Plateforme (Vinted, Leboncoin, etc.)
- condition : État (Neuf, Très bon, etc.)
- purchase_price : Prix d'achat
- selling_price : Prix de vente
- fees : Frais (commissions, etc.)
- quantity : Quantité
- status : Statut (STOCK, EN_VENTE, VENDU)
- date_added : Date d'ajout
- date_sold : Date de vente
- notes : Notes personnelles
- image_path : Chemin vers l'image (optionnel)

## 🎮 Guide d'Utilisation

### Ajouter un produit

1. Cliquez sur **"➕ Ajouter Produit"** dans la sidebar
2. Remplissez les champs du formulaire
3. Cliquez sur **"📊 Calculer Bénéfice Estimé"** pour voir le profit attendu
4. Cliquez sur **"✓ Ajouter Produit"**

### Gérer les produits

1. Allez sur **"📦 Produits"**
2. Utilisez les filtres (En Stock, En Vente, Vendus, Tous)
3. Recherchez par nom/catégorie
4. **✓ Vendre** : Marque comme vendu
5. **✕** : Supprime le produit

### Consulter le Dashboard

1. Cliquez sur **"📈 Dashboard"**
2. Consultez les KPIs principaux et statistiques
3. Analysez les profit par catégorie

## 💡 Données de Test

L'application inclut 5 produits de test pour sa première utilisation :

- Jean Levi's 501
- Nike Air Force 1
- Louis Vuitton Speedy
- T-shirt Vintage Nirvana
- PlayStation 5 Manette

Ces données sont ajoutées automatiquement au premier lancement.

## 🔧 Configuration

Modifiez `config.py` pour personnaliser :

- Couleurs de l'interface
- Catégories de produits
- Conditions disponibles
- Plateformes de vente

## 📦 Dépendances

```
customtkinter>=5.0.0
```

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'customtkinter'"

Installez les dépendances :

```bash
pip install -r requirements.txt
```

### La base de données ne se crée pas

Vérifiez que vous avez les droits d'écriture dans le dossier.

### L'application plante au démarrage

Vérifiez que Python 3.8+ est installé :

```bash
python --version
```

## 🚀 Améliorations Futures

- [ ] Gestion des images avec aperçu
- [ ] Export en CSV/Excel
- [ ] Graphiques de tendance
- [ ] Sauvegarde/restauration de base de données
- [ ] API d'intégration Vinted
- [ ] Notifications de prix

## 📝 Licence

Libre d'utilisation pour usage personnel

## 👨‍💻 Auteur

Créé avec ❤️ pour la gestion simplifiée du stock Vinted
