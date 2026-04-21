"""
Service de gestion des finances et calculs
"""
from typing import List
from vinted_app.database.db import DatabaseManager
from vinted_app.database.models import Product


class FinanceService:
    """Service pour les calculs financiers"""

    def __init__(self, db: DatabaseManager):
        """Initialise le service"""
        self.db = db

    def get_total_invested(self) -> float:
        """Calcule le montant total investi"""
        products = self.db.get_all_products()
        total = 0
        for product in products:
            if product.status != "VENDU":
                total += product.purchase_price * product.quantity
        return round(total, 2)

    def get_total_earned(self) -> float:
        """Calcule le total gagné avec les ventes"""
        products = self.db.get_products_by_status("VENDU")
        total = 0
        for product in products:
            total += product.selling_price * product.quantity
        return round(total, 2)

    def get_total_fees(self) -> float:
        """Calcule le total des frais"""
        products = self.db.get_products_by_status("VENDU")
        total = 0
        for product in products:
            total += product.fees * product.quantity
        return round(total, 2)

    def get_total_profit(self) -> float:
        """Calcule le bénéfice total"""
        return round(self.get_total_earned() - self.get_total_fees() - self.get_total_invested_sold(), 2)

    def get_total_invested_sold(self) -> float:
        """Calcule le montant investi pour les produits vendus"""
        products = self.db.get_products_by_status("VENDU")
        total = 0
        for product in products:
            total += product.purchase_price * product.quantity
        return round(total, 2)

    def get_profit_margin_percent(self) -> float:
        """Calcule la marge de profit en pourcentage"""
        total_earned = self.get_total_earned()
        if total_earned == 0:
            return 0
        total_profit = self.get_total_profit()
        return round((total_profit / total_earned) * 100, 2)

    def get_average_product_profit(self) -> float:
        """Calcule le bénéfice moyen par produit"""
        products = self.db.get_products_by_status("VENDU")
        if not products:
            return 0
        total_profit = 0
        count = 0
        for product in products:
            total_profit += (product.selling_price - product.purchase_price - product.fees) * product.quantity
            count += product.quantity
        return round(total_profit / count if count > 0 else 0, 2)

    def get_profit_by_category(self) -> dict:
        """Calcule le profit par catégorie"""
        products = self.db.get_products_by_status("VENDU")
        profit_by_category = {}

        for product in products:
            if product.category not in profit_by_category:
                profit_by_category[product.category] = 0
            profit = (product.selling_price - product.purchase_price - product.fees) * product.quantity
            profit_by_category[product.category] += profit

        return {k: round(v, 2) for k, v in profit_by_category.items()}

    def get_roi(self) -> float:
        """Calcule le ROI (Return on Investment) en pourcentage"""
        total_invested_sold = self.get_total_invested_sold()
        if total_invested_sold == 0:
            return 0
        total_profit = self.get_total_profit()
        return round((total_profit / total_invested_sold) * 100, 2)
