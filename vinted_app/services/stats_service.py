"""
Service de statistiques
"""
from typing import Dict, List
from vinted_app.database.db import DatabaseManager
from vinted_app.database.models import Product


class StatsService:
    """Service pour les statistiques"""

    def __init__(self, db: DatabaseManager):
        """Initialise le service"""
        self.db = db

    def get_general_stats(self) -> dict:
        """Récupère les statistiques générales"""
        products = self.db.get_all_products()
        
        stats = {
            "total_products": len(products),
            "total_quantity": sum(p.quantity for p in products),
            "in_stock": len(self.db.get_products_by_status("STOCK")),
            "in_sale": len(self.db.get_products_by_status("EN_VENTE")),
            "sold": len(self.db.get_products_by_status("VENDU")),
        }
        return stats

    def get_category_stats(self) -> Dict[str, int]:
        """Récupère les statistiques par catégorie"""
        products = self.db.get_all_products()
        stats = {}

        for product in products:
            if product.category not in stats:
                stats[product.category] = 0
            stats[product.category] += product.quantity

        return dict(sorted(stats.items()))

    def get_platform_stats(self) -> Dict[str, int]:
        """Récupère les statistiques par plateforme"""
        products = self.db.get_all_products()
        stats = {}

        for product in products:
            if product.platform not in stats:
                stats[product.platform] = 0
            stats[product.platform] += product.quantity

        return dict(sorted(stats.items()))

    def get_status_stats(self) -> Dict[str, int]:
        """Récupère les statistiques par statut"""
        return {
            "STOCK": len(self.db.get_products_by_status("STOCK")),
            "EN_VENTE": len(self.db.get_products_by_status("EN_VENTE")),
            "VENDU": len(self.db.get_products_by_status("VENDU")),
        }

    def get_top_profitable_products(self, limit: int = 5) -> List[dict]:
        """Récupère les produits les plus rentables"""
        products = self.db.get_products_by_status("VENDU")
        
        profitable = []
        for product in products:
            profitable.append({
                "name": product.name,
                "profit": round(product.get_profit() * product.quantity, 2),
                "margin": round(product.get_margin_percent(), 2)
            })

        profitable.sort(key=lambda x: x["profit"], reverse=True)
        return profitable[:limit]

    def get_least_profitable_products(self, limit: int = 5) -> List[dict]:
        """Récupère les produits les moins rentables"""
        products = self.db.get_products_by_status("VENDU")
        
        profitable = []
        for product in products:
            profitable.append({
                "name": product.name,
                "profit": round(product.get_profit() * product.quantity, 2),
                "margin": round(product.get_margin_percent(), 2)
            })

        profitable.sort(key=lambda x: x["profit"])
        return profitable[:limit]

    def get_average_stats(self) -> dict:
        """Récupère les statistiques moyennes"""
        products = self.db.get_all_products()
        sold_products = self.db.get_products_by_status("VENDU")

        if not products:
            return {
                "avg_purchase": 0,
                "avg_selling": 0,
                "avg_profit": 0
            }

        avg_purchase = sum(p.purchase_price for p in products) / len(products)
        
        if not sold_products:
            return {
                "avg_purchase": round(avg_purchase, 2),
                "avg_selling": 0,
                "avg_profit": 0
            }

        avg_selling = sum(p.selling_price for p in sold_products) / len(sold_products)
        avg_profit = sum(p.get_profit() for p in sold_products) / len(sold_products)

        return {
            "avg_purchase": round(avg_purchase, 2),
            "avg_selling": round(avg_selling, 2),
            "avg_profit": round(avg_profit, 2)
        }
