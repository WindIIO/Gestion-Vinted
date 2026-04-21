"""
Utilités et fonctions auxiliaires
"""
import os
from datetime import datetime


def format_currency(amount: float) -> str:
    """Formate un montant en devise"""
    return f"{amount:,.2f}€"


def format_percentage(value: float) -> str:
    """Formate un pourcentage"""
    return f"{value:.2f}%"


def format_date(date_string: str) -> str:
    """Formate une date"""
    if not date_string:
        return "-"
    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d %H:%M:%S")
        return date_obj.strftime("%d/%m/%Y")
    except:
        return date_string


def get_asset_path(filename: str) -> str:
    """Retourne le chemin complet d'un fichier asset"""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_dir, "assets", filename)


def truncate_text(text: str, max_length: int = 50) -> str:
    """Tronque un texte si trop long"""
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text


def get_status_color(status: str) -> str:
    """Retourne la couleur correspondant au statut"""
    colors = {
        "STOCK": "#6B7280",        # Gris
        "EN_VENTE": "#F59E0B",     # Orange
        "VENDU": "#22C55E"         # Vert
    }
    return colors.get(status, "#3B82F6")


def get_status_label(status: str) -> str:
    """Retourne l'étiquette du statut"""
    labels = {
        "STOCK": "En Stock",
        "EN_VENTE": "En Vente",
        "VENDU": "Vendu"
    }
    return labels.get(status, status)
