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
        return self.db.add_product(product)

    def get_all_products(self) -> List[Product]:
        """Récupère tous les produits"""
        return self.db.get_all_products()

    def get_product(self, product_id: int) -> Optional[Product]:
        """Récupère un produit par ID"""
        return self.db.get_product_by_id(product_id)

    def get_products_by_status(self, status: str) -> List[Product]:
        """Récupère les produits par statut"""
        return self.db.get_products_by_status(status)

    def update_product(self, product_id: int, **kwargs) -> bool:
        """Met à jour un produit"""
        product = self.db.get_product_by_id(product_id)
        if not product:
            return False

        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)

        return self.db.update_product(product)

    def change_product_status(self, product_id: int, new_status: str) -> bool:
        """Change le statut d'un produit"""
        return self.db.update_product_status(product_id, new_status)

    def delete_product(self, product_id: int) -> bool:
        """Supprime un produit"""
        return self.db.delete_product(product_id)

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
