"""
Service de gestion des produits
"""
from typing import List, Optional
from vinted_app.database.db import DatabaseManager
from vinted_app.database.models import Product


class ProductService:
    """Service pour la gestion des produits"""

    def __init__(self, db: DatabaseManager):
        """Initialise le service"""
        self.db = db
        self._cache = {}
        self._cache_valid = False

    def _invalidate_cache(self):
        """Invalide le cache"""
        self._cache_valid = False
        self._cache = {}

    def _get_cached_products(self, key: str, fetch_func):
        """Récupère les produits depuis le cache ou la DB"""
        if not self._cache_valid or key not in self._cache:
            self._cache[key] = fetch_func()
        return self._cache.get(key, [])

    def create_product(self, name: str, category: str, platform: str,
                      condition: str, purchase_price: float,
                      selling_price: float, fees: float,
                      quantity: int = 1, status: str = "STOCK",
                      notes: str = "") -> int:
        """Crée et ajoute un produit"""
        product = Product(
            name=name,
            category=category,
            platform=platform,
            condition=condition,
            purchase_price=purchase_price,
            selling_price=selling_price,
            fees=fees,
            quantity=quantity,
            status=status,
            notes=notes
        )
        product_id = self.db.add_product(product)
        if product_id:
            self._invalidate_cache()
        return product_id

    def get_all_products(self) -> List[Product]:
        """Récupère tous les produits"""
        return self._get_cached_products("all", self.db.get_all_products)

    def get_product(self, product_id: int) -> Optional[Product]:
        """Récupère un produit par ID"""
        return self.db.get_product_by_id(product_id)

    def get_products_by_status(self, status: str) -> List[Product]:
        """Récupère les produits par statut"""
        return self._get_cached_products(f"status_{status}", lambda: self.db.get_products_by_status(status))

    def update_product(self, product_id: int, **kwargs) -> bool:
        """Met à jour un produit"""
        product = self.db.get_product_by_id(product_id)
        if not product:
            return False

        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)

        success = self.db.update_product(product)
        if success:
            self._invalidate_cache()
        return success

    def change_product_status(self, product_id: int, new_status: str) -> bool:
        """Change le statut d'un produit"""
        success = self.db.update_product_status(product_id, new_status)
        if success:
            self._invalidate_cache()
        return success

    def delete_product(self, product_id: int) -> bool:
        """Supprime un produit"""
        success = self.db.delete_product(product_id)
        if success:
            self._invalidate_cache()
        return success

    def search_products(self, query: str) -> List[Product]:
        """Recherche des produits"""
        return self.db.search_products(query)

    def get_stock_count(self) -> int:
        """Retourne le nombre de produits en stock"""
        products = self.db.get_products_by_status("STOCK")
        return sum(p.quantity for p in products)

    def get_in_sale_count(self) -> int:
        """Retourne le nombre de produits en vente"""
        products = self.db.get_products_by_status("EN_VENTE")
        return sum(p.quantity for p in products)

    def get_sold_count(self) -> int:
        """Retourne le nombre de produits vendus"""
        products = self.db.get_products_by_status("VENDU")
        return sum(p.quantity for p in products)
