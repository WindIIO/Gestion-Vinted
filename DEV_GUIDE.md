# 👨‍💻 GUIDE DE DÉVELOPPEMENT

## Architecture de l'Application

```
Model -> Service -> UI
  ↓        ↓         ↓
 DB      Logic     Display
```

### Couches

#### 1. **Database Layer** (`database/`)

- `models.py`: Classe `Product` avec méthodes utiles
- `db.py`: `DatabaseManager` pour toutes opérations SQLite

#### 2. **Service Layer** (`services/`)

- `product_service.py`: Gestion CRUD des produits
- `finance_service.py`: Calculs financiers (profit, ROI, etc.)
- `stats_service.py`: Statistiques et analyses

#### 3. **UI Layer** (`ui/`)

- `main_window.py`: Fenêtre principale et routing
- `dashboard.py`: Vue dashboard
- `product_list.py`: Vue liste et filtres
- `add_product.py`: Vue formulaire

#### 4. **Utilities** (`utils/`)

- `helpers.py`: Formatage, conversions, etc.

---

## Ajouter une Nouvelle Fonctionnalité

### Exemple: Ajouter un filtre par prix

#### 1. Ajouter dans `product_service.py`:

```python
def get_products_by_price_range(self, min_price: float, max_price: float):
    """Récupère les produits par gamme de prix"""
    products = self.db.get_all_products()
    return [p for p in products
            if min_price <= p.selling_price <= max_price]
```

#### 2. Ajouter dans `product_list.py`:

```python
# Dans _create_ui():
price_min = ctk.CTkEntry(..., placeholder_text="Prix min")
price_max = ctk.CTkEntry(..., placeholder_text="Prix max")

# Callback
def _filter_by_price():
    products = self.product_service.get_products_by_price_range(
        float(price_min.get() or 0),
        float(price_max.get() or 99999)
    )
    # Afficher les produits
```

---

## Modifier l'Apparence

### Couleurs (`config.py`)

```python
COLORS = {
    "bg_primary": "#1a1a1a",      # Fond principal
    "accent": "#0066FF",           # Couleur d'accent
    "success": "#22C55E",          # Vert
    # ...
}
```

### Polices (`ui/*.py`)

```python
# Changer tous les "Arial" en une autre police
font=("Segoe UI", 12, "bold")
```

---

## Données de Test (`config.py`)

Modifier `SAMPLE_PRODUCTS` pour pré-charger d'autres produits:

```python
SAMPLE_PRODUCTS = [
    {
        "name": "Votre produit",
        "category": "Catégorie",
        "platform": "Vinted",
        "condition": "Neuf",
        "purchase_price": 50.0,
        "selling_price": 100.0,
        "fees": 10.0,
        "quantity": 1,
        "status": "STOCK",
        "notes": "Description"
    },
]
```

---

## Ajout d'une Nouvelle Page

### 1. Créer `ui/new_page.py`:

```python
import customtkinter as ctk
from vinted_app import config

class NewPageFrame(ctk.CTkFrame):
    def __init__(self, parent, refresh_callback):
        super().__init__(parent, fg_color=config.COLORS["bg_primary"])
        self.refresh_callback = refresh_callback
        self._create_ui()

    def _create_ui(self):
        # Votre UI
        pass

    def refresh(self):
        # Rafraîchissement
        pass
```

### 2. Importer dans `main_window.py`:

```python
from vinted_app.ui.new_page import NewPageFrame

# Dans _create_ui():
self.frames['new_page'] = NewPageFrame(...)
self.frames['new_page'].grid(...)
```

### 3. Ajouter bouton de navigation:

```python
buttons = [
    # ...
    ("🆕 Nouvelle Page", "new_page"),
]
```

---

## Testing

### Test manuel:

```bash
python vinted_app/main.py
```

### Test automatisé:

```bash
python test_app.py
```

### Test spécifique:

```python
from vinted_app.database.db import DatabaseManager
from vinted_app.services.finance_service import FinanceService

db = DatabaseManager()
finance = FinanceService(db)
print(finance.get_total_profit())
```

---

## Bonnes Pratiques

### ✅ À Faire

- Utiliser les services plutôt que la DB directement dans l'UI
- Ajouter des commentaires pour les fonctions complexes
- Valider les inputs de l'utilisateur
- Rafraîchir l'UI après modification de données
- Faire des commits petits et atomiques

### ❌ À Éviter

- Logique métier dans l'UI
- Requêtes DB directes dans les vues
- Variables globales
- Code dupliqué
- Pas de gestion d'erreurs

---

## Structure Types des Fichiers

### Service

```python
class MyService:
    def __init__(self, db: DatabaseManager):
        self.db = db

    def operation(self, param):
        # Logique métier
        return result
```

### UI Frame

```python
class MyFrame(ctk.CTkFrame):
    def __init__(self, parent, service, refresh_callback):
        super().__init__(parent, fg_color=config.COLORS["bg_primary"])
        self.service = service
        self.refresh_callback = refresh_callback
        self._create_ui()

    def _create_ui(self):
        # Créer les widgets
        pass

    def refresh(self):
        # Rafraîchir les données
        pass
```

---

## Déploiement

### Créer un exécutable (PyInstaller)

```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name "VintedStockManager" vinted_app/main.py
```

### Créer un installeur (Windows)

Utiliser NSIS ou Inno Setup avec le fichier `.exe` généré.

---

## Ressources

- CustomTkinter: https://github.com/TomSchimansky/CustomTkinter
- SQLite: https://www.sqlite.org/
- Python Docs: https://docs.python.org/3/

---

## Support & Contact

Pour toute question:

1. Vérifiez la structure du projet
2. Testez avec `python test_app.py`
3. Consultez les commentaires du code
