"""
Modèles de données pour la base de données
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class Product:
    """Classe représentant un produit"""
    name: str
    category: str
    platform: str
    condition: str
    purchase_price: float
    selling_price: float
    fees: float
    quantity: int = 1
    status: str = "STOCK"
    notes: str = ""
    image_path: Optional[str] = None
    id: Optional[int] = None
    date_added: Optional[str] = None
    date_sold: Optional[str] = None

    def get_profit(self) -> float:
        """Calcule le bénéfice"""
        return self.selling_price - self.purchase_price - self.fees

    def get_margin_percent(self) -> float:
        """Calcule la marge en pourcentage"""
        if self.selling_price == 0:
            return 0
        return (self.get_profit() / self.selling_price) * 100

    def to_dict(self):
        """Convertit l'objet en dictionnaire"""
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'platform': self.platform,
            'condition': self.condition,
            'purchase_price': self.purchase_price,
            'selling_price': self.selling_price,
            'fees': self.fees,
            'quantity': self.quantity,
            'status': self.status,
            'notes': self.notes,
            'image_path': self.image_path,
            'date_added': self.date_added,
            'date_sold': self.date_sold
        }

    @classmethod
    def from_dict(cls, data: dict):
        """Crée un Product à partir d'un dictionnaire"""
        return cls(
            id=data.get('id'),
            name=data.get('name'),
            category=data.get('category'),
            platform=data.get('platform'),
            condition=data.get('condition'),
            purchase_price=data.get('purchase_price', 0),
            selling_price=data.get('selling_price', 0),
            fees=data.get('fees', 0),
            quantity=data.get('quantity', 1),
            status=data.get('status', 'STOCK'),
            notes=data.get('notes', ''),
            image_path=data.get('image_path'),
            date_added=data.get('date_added'),
            date_sold=data.get('date_sold')
        )
